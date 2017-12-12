#!/usr/bin/env python

"""
Usage:

    pip install -r requirements.txt
    python update_multiple_issues.py

Notes:

- Use this script to update/add custom issue fields for each issue.
"""

import click
import requests
import json

API_ENDPOINT = "https://api.helpshift.com/v1/{}/issues"

# Add CIF key, type and value which should be added/updated for each issue.
CIFS_KEY_VALUES = {"cif_key": {"type": "cif_type", "value": "cif_value"}}


def update_cifs_of_issues(domain, api_key, issues, page):
    updated_issues_count = 0
    issue_ids = map(lambda issue: issue["id"], issues)
    api_params = {"custom_fields": json.dumps(CIFS_KEY_VALUES),
                  "issue-ids": json.dumps(issue_ids)}
    api_response = requests.put(API_ENDPOINT.format(domain),
                                data=api_params,
                                auth=(api_key, ""))
    api_response.raise_for_status()
    updated_issues_count += len(issue_ids)
    click.echo("Updated {} issues in page number {}.".format(updated_issues_count, page))


@click.command()
@click.option("--domain",
              prompt="Domain",
              help="The domain name to fetch issues for")
@click.option("--api-key",
              prompt="API Key",
              help="The API key for the domain")
def fetch_and_update_issues(domain, api_key):
    current_page = 0
    api_params = {"page-size": 1000,
                  "includes": json.dumps(["meta"]),
                  "sort-by": "creation-time",
                  "sort-order": "desc"}
    while True:
        current_page += 1
        api_params['page'] = current_page
        api_response = requests.get(url=API_ENDPOINT.format(domain),
                                    params=api_params,
                                    auth=(api_key, ""))
        api_response.raise_for_status()
        parsed_response = api_response.json()
        click.echo("Fetched page {}/{}".format(current_page, parsed_response['total-pages']))
        update_cifs_of_issues(domain, api_key, parsed_response["issues"], current_page)
        if parsed_response["total-pages"] == current_page:
            click.echo("Issues update completed.")
            break


if __name__ == "__main__":
    fetch_and_update_issues()
