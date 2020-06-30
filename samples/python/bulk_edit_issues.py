import requests
import json

page_size = 1000 #max value
page = 0
api_key = "<api-key>"
endpoint = "https://api.helpshift.com/v1/<domain>/issues"

def bulk_edit_issue(issues):
    print ("Triggering Bulk Action for " + str(len(issues)) + " issues")
    api_params = {"issue-ids": json.dumps([issue['id'] for issue in issues]),
                  "status": "Resolved",
                  "message-body": "Your order will reach you soon!"}
    response = requests.put(endpoint,
                            params=api_params,
                            auth=(api_key, ""))
    response.raise_for_status()


while True:
    page += 1
    api_params = {"sort-by": "creation-time",
                  "sort-order": "asc",
                  "page-size": page_size,
                  "page": page}
    response = requests.get(endpoint,
                            params = api_params,
                            auth = (api_key, ""))
    # Fail fast
    response.raise_for_status()
    data = response.json()

    # All the issues for the given query
    issues = data['issues']

    # Result returned no issues.
    if not issues:
        print("No matching issues. Done")
        break

    bulk_edit_issue(issues)

    #This is perhaps the last chunk of issues since
    #the count is less than the requested page size
    if len(issues) < page_size:
       print('Processed last chunk')
       break
