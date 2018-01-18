#!/usr/bin/env python

"""
Usage:
    pip install -r requirements.txt
    python issues_with_custom_issue_fields.py
        enter domain, api key and action to perform.
    
Notes:
    - Custom issue fields (CIFs) of all types have been considered in this example.
    - This program allows a user to create and retrieve issues with CIFs.
    - Create issues option will create issues having different values for each CIF.
    - Please refer PAYLOADS in "./custom_issue_field_payloads.py" for CIFs that are used for these issues.
    - Get issues will retrieve issues depending on a variety of filter conditions.
    - Please refer FILTERS in "./custom_issue_field_payloads.py" for details.
    - All possible conditions on all types of CIFs have been used here.
    - Please refer the API documentation for further details on how to use CIFs while creating or retrieving an issue.
"""

import requests
import click
import json
import time

import custom_issue_field_payloads

ISSUES_ENDPOINT = 'https://api.helpshift.com/v1/{0}/issues'


def create_an_issue(endpoint, api_key, payload):
    response = requests.post(endpoint, auth=(api_key, ""), data=payload)
    if response.status_code != 201:
        click.echo("Something went wrong while creating issue:" + "\nPayload: " + str(payload) + "\nResponse: " +
                   str(response.json()))
        exit(1)
    click.echo("Issue created, with custom fields: " + str(response.json()["custom_fields"]))
    return


def get_issues(endpoint, api_key, params):
    response = requests.get(endpoint, auth=(api_key, ""), params=params)
    if response.status_code != 200:
        click.echo("Something went wrong in retrieval:" + "\nCondition: " + str(params) + "\nResponse: " +
                   str(response.json()))
        exit(1)
    return response.json()


def create_issues(domain, api_key):
    endpoint = ISSUES_ENDPOINT.format(domain)
    for cif_payload in custom_issue_field_payloads.PAYLOADS:
        payload = custom_issue_field_payloads.BASIC_PAYLOAD
        payload.update({"custom_fields": json.dumps(cif_payload)})
        create_an_issue(endpoint, api_key, payload)
    time.sleep(10)


def retrieve_issues(domain, api_key):
    while True:

        print '\nAvailable filters:'
        for num, item in enumerate(custom_issue_field_payloads.FILTERS):
            print '{0}. {1}'.format(num, item['description'])

        try:
            try_filter = raw_input('\nEnter the filter number or -1 to quit: ')
            if try_filter == '-1':
                exit(0)

            filter_condition = custom_issue_field_payloads.FILTERS[int(try_filter)]
            resp = get_issues(ISSUES_ENDPOINT.format(domain), api_key,
                              {"custom_fields": json.dumps(filter_condition["query"]),
                               "state": "new",
                               "includes": json.dumps(["custom_fields"])})

            print ("\n\nCondition: {0}\nNumber of issues: {1}\nIssues:\n{2}"
                   .format(filter_condition["description"], str(resp["total-hits"]), str(resp["issues"])))
        except (ValueError, IndexError):
            print ('Invalid filter number. Try again')


@click.command()
@click.option('--domain',
              prompt='Domain',
              help='The domain to create issues for')
@click.option('--api-key',
              prompt='API key',
              help='The API key for the domain')
@click.option('--type_of_action',
              help='Create or Retrieve Issues',
              type=click.Choice(['create', 'get', 'exit']), prompt='What to do? create / get / exit')
def action(domain, api_key, type_of_action):
    if type_of_action == 'create':
        create_issues(domain, api_key)
    elif type_of_action == 'get':
        retrieve_issues(domain, api_key)
    else:
        exit(0)


if __name__ == "__main__":
    action()
