#!/usr/bin/env python

"""
Usage:

    pip install -r requirements.txt
    python export_issues_to_csv.py

Notes:

- Messages are exported to a different file for ease of access.
- Each message row will have its corresponding issue id.
- The API will fetch 1000 (maximum allowed) issues per call, as specified in the "api_endpoint" below.
- Total number of API calls is equal to the number of total pages in the responses.
- To limit the total size of response, the program takes number of days N as input.
  Issues created in the last N days will be fetched. To get ALL issues, remove the parameter "created_since".
- A few fields of the response json that may not be important have not been considered in this sample.
- Please refer the documentation for the complete response structure.
- Outbound Messages counts include agents and automation messages counts.
- Inbound Messages counts just include end-user messages counts.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import os

import arrow
import click
import requests
import unicodecsv as csv


ISSUES_FILE_NAME = 'issues.csv'
MESSAGES_FILE_NAME = 'messages.csv'
ISSUES_FIELD_NAMES = ['domain', 'app_id', 'state', 'changed_at', 'assignee_name', 'id', 'title', 'tags',
                      'inbound_messages_count,', 'outbound_messages_count']
MESSAGE_FIELD_NAMES = ['issue_id', 'author', 'body', 'attachment']
ISSUES_API_URL = 'https://api.helpshift.com/v1/{}/issues'


def fetch_issues(api_key, api_params, api_url, current_page):
    api_params['page'] = current_page
    raw_response = requests.get(api_url, params=api_params, auth=(api_key, ''))
    raw_response.raise_for_status()
    return raw_response.json()


def count_inbound_and_outbound_messages(messages):
    inbound_count, outbound_count = 0, 0
    for message in messages:
        if message['origin'] == 'end-user':
            inbound_count += 1
        elif message['origin'] == 'helpshift':
            outbound_count += 1
    return inbound_count, outbound_count


def construct_issues_file_row(issue):
    inbound_count, outbound_count = count_inbound_and_outbound_messages(issue['messages'])
    return dict(issue,
                assignee_name=issue.get('assignee_name', ''),
                title=issue.get('title', ''),
                state=issue['state_data']['state'],
                tags='|'.join(issue['tags']),
                changed_at=issue['state_data']['changed_at'],
                inbound_messages=inbound_count,
                outbound_messages=outbound_count)


def construct_messages_file_row(issue_id, message):
    return dict(issue_id=issue_id,
                body=message['body'],
                author=message['author']['name'],
                attachment=message.get('attachment', {}).get('file_name'))


@click.command()
@click.option('--domain',
              prompt='Domain',
              help='The domain to fetch issues for')
@click.option('--api-key',
              prompt='API key',
              help='The API key for the domain')
@click.option('--days',
              prompt='Number of days',
              default=30,
              type=int,
              help='Last N days to fetch issues for')
@click.option('--output-directory',
              prompt=True,
              default=os.getcwd,
              type=click.Path(exists=True, dir_okay=True, file_okay=False, writable=True, resolve_path=True),
              help='The directory under which we will store CSV files')
def export_issues_to_csv(domain, api_key, days, output_directory):
    timestamp_in_ms = arrow.utcnow().replace(days=-days).timestamp * 1000
    api_url = ISSUES_API_URL.format(domain)
    issues_path = os.path.join(output_directory, ISSUES_FILE_NAME)
    messages_path = os.path.join(output_directory, MESSAGES_FILE_NAME)

    with open(issues_path, 'wb') as issues_file, open(messages_path, 'wb') as messages_file:
        issue_writer = csv.DictWriter(issues_file, fieldnames=ISSUES_FIELD_NAMES, extrasaction='ignore', restval='')
        message_writer = csv.DictWriter(messages_file, fieldnames=MESSAGE_FIELD_NAMES, extrasaction='ignore', restval='')
        issue_writer.writeheader()
        message_writer.writeheader()

        current_page = 0

        # See https://apidocs.helpshift.com/#!/Issues/get_issues for more parameters
        api_params = {
            'created-since': timestamp_in_ms,
            'page-size': 1000
        }

        while True:
            current_page += 1
            response = fetch_issues(api_key, api_params, api_url, current_page)
            click.echo("Fetched page {}/{}".format(current_page, response['total-pages']))

            for issue in response['issues']:
                issue_writer.writerow(construct_issues_file_row(issue))

                for message in issue['messages']:
                    message_writer.writerow(construct_messages_file_row(issue['id'], message))

            if response['total-pages'] == current_page:
                click.echo('Export completed.')
                break


if __name__ == '__main__':
    export_issues_to_csv()
