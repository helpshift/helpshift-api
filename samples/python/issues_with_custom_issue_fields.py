#!/usr/bin/env python

"""
Usage:
    pip install -r requirements.txt
    python issues_with_custom_issue_fields.py
    
Notes:
    - Custom issue fields (CIFs) of all types have been considered in this example.
    - Issues having different values for each CIF are initially created. Please refer PAYLOADS in 
    "./custom_issue_field_payloads.py" that are used for these issues.
    - These issues are then retrieved depending on a variety of filter conditions. Please refer FILTERS in
    "./custom_issue_field_payloads.py" for details.
    - All possible conditions on all types of CIFs have been used here.
    - Please refer the API documentation for details on how to use CIFs while creating or retrieving an issue.
"""

import requests
import click
import json
import time

import custom_issue_field_payloads


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


@click.command()
@click.option('--domain',
              prompt='Domain',
              help='The domain to create issues for')
@click.option('--api-key',
              prompt='API key',
              help='The API key for the domain')
def create_and_retrieve_issues(domain, api_key):
    issues_endpoint = 'https://api.helpshift.com/v1/{0}/issues'.format(domain)

    for cif_payload in custom_issue_field_payloads.PAYLOADS:
        payload = custom_issue_field_payloads.BASIC_PAYLOAD
        payload.update({"custom_fields": json.dumps(cif_payload)})
        create_an_issue(issues_endpoint, api_key, payload)

    time.sleep(10)

    for filter_condition in custom_issue_field_payloads.FILTERS:
        resp = get_issues(issues_endpoint, api_key, {"custom_fields": json.dumps(filter_condition["query"]),
                                                     "state": "new",
                                                     "includes": json.dumps(["custom_fields"])})

        click.echo("\n\nCondition: {0}\nNumber of issues: {1}\nIssues:\n{2}"
          .format(filter_condition["description"], str(resp["total-hits"]), str(resp["issues"])))


if __name__ == "__main__":
    create_and_retrieve_issues()
