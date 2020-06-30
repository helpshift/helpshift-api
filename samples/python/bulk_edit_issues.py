import requests
import json

DOMAIN = "<DOMAIN>"
API_KEY = "<api-key>"
ENDPOINT = "https://api.helpshift.com/v1/" + DOMAIN + "/issues"

PAGE_SIZE = 1000 #max value

# Add to `api_params` to edit issues as per your requirement.

def bulk_edit_issue(issues):
    print ("Triggering Bulk Action for %d issues starting with id %s and ends with id %d" %((len(issues)), issues[0], issues[-1]))
    api_params = "/?issue-ids=" + json.dumps(issues) + "&status=Resolved" #example
    response = requests.put((ENDPOINT + api_params), auth=(API_KEY, ""))
    response.raise_for_status()


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
        issues = (data['issues'])

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


# By default queries from GET API and performs bulk action
if __name__ == "__main__":
    process_issues_from_get_api()
