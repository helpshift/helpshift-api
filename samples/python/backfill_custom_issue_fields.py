#!/usr/bin/env python

"""
Usage:

    pip install -r requirements.txt
    python backfill_custom_issue_fields.py

Notes:

- Use this script to update custom issue fields with the metadata values.
- This script expects that metadata fields to custom issue fields mapping is
  already defined in Helpshift dashboard.
"""

import click
import requests
import json

API_ENDPOINT = "https://api.helpshift.com/v1/{}/issues"

# Update this mapping with the metadata keys to Custom Issue Fields as defined
# in the Helpshift dashboard.
METADATA_CIFS_MAPPINGS = {"metadata_key1": "cif_key1", "metadata_key2": "cif_key2"}


def construct_cif_from_metadata(metadata):
    custom_issue_fields = {}
    for key, value in metadata.items():
        if key in METADATA_CIFS_MAPPINGS:
            cif_key = METADATA_CIFS_MAPPINGS[key]
            cif_value = value if type(value).__name__ == "unicode" else str(value)
            custom_issue_fields[cif_key] = {"type": "singleline", "value": cif_value}
    return custom_issue_fields


def update_cifs_of_issues(domain, api_key, issues, page):
    updated_issues_count = 0
    for issue in issues:
        cifs = construct_cif_from_metadata(issue['meta'])
        if cifs:
            api_params = {"custom_fields": json.dumps(cifs)}
            api_url = API_ENDPOINT + "/{}"
            api_response = requests.put(api_url.format(domain, issue["id"]),
                                        data=api_params,
                                        auth=(api_key, ""))
            api_response.raise_for_status()
            updated_issues_count += 1
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
