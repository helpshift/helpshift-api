import requests
import json
import csv
import base64

DOMAIN = "<DOMAIN>"
API_KEY = "<api-key>"
ENDPOINT = "https://api.helpshift.com/v1/" + DOMAIN + "/issues"

PAGE_SIZE = 1000 #max value
BULK_CHUNK = 5000 #max value

# Add to `api_params` to edit issues as per your requirement.

def bulk_edit_issue(issues):
    print ("Triggering Bulk Action for %d issues starting with id %s and ends with id %d" %((len(issues)), issues[0], issues[-1]))
    api_params = {"issue-ids" : json.dumps(issues),
                  "message-body" : "Your order will reach you shortly!", #example
                  "status" : "Resolved"} #example
    headers = {
        'Authorization': 'Basic ' + base64.b64encode(API_KEY+':'),
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    response = requests.put(ENDPOINT,
                            headers = headers,
                            data = api_params)
    response.raise_for_status()
    # closing the connection
    response.close()


# Query from GET /issues API
# Add to `api_params` to get issues to match filters of your choice.

def process_issues_from_get_api():
    CURRENT_PAGE = 1
    while True:
        api_params = {"sort-by": "creation-time",
                      "sort-order": "asc",
                      "page-size": PAGE_SIZE,
                      "page": CURRENT_PAGE}
        response = requests.get(ENDPOINT,
                                params = api_params,
                                auth = (API_KEY, ""))
        # Fail fast
        response.raise_for_status()
        data = response.json()

        # All the issues for the given query
        issues = data['issues']

        # Result returned no issues.
        if not issues:
            print("No matching issues. Done")
            break

        bulk_edit_issue([issue['id'] for issue in issues])

        #This is perhaps the last chunk of issues since
        #the count is less than the requested page size
        if len(issues) < PAGE_SIZE:
            print('Processed last chunk')
            break

        CURRENT_PAGE += 1


# Expects:
# I. CSV delimited by comma ","
# II. Issue publish IDs to be part of the first column in the CSV
# Example:
# 1, .....
# 2, .....
# 3, .....

# use process_issues_from_csv(<absolute file path>)

def process_issues_from_csv(csv_path):
    issue_ids = []
    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            issue_ids.append(row[0])
    issue_chunks = [issue_list[i:i + BULK_CHUNK] for i in range(0, len(issue_list), BULK_CHUNK)]
    for issue_chunk in issue_chunks:
        bulk_edit_issue(issue_chunk)
    print ("Done")


# By default queries from GET API and performs bulk action
if __name__ == "__main__":
    process_issues_from_get_api()
