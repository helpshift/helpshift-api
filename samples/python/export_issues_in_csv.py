import requests
import csv


DOMAIN = "<DOMAIN>"
API_KEY = "<API_KEY>"
ISSUES_FILE_LOC = "<ISSUES_FILE_LOCATION>/issues.csv"
MESSAGES_FILE_LOC = "<MESSAGES_FILE_LOCATION>/messages.csv"


'''
POINTS TO NOTE:
- Messages are exported to a different file for ease of access.
- Each message row will have its corresponding issue id.
- The API will fetch 1000 (maximum allowed) issues per call, as specified in the 'api_endpoint' below.
- Total number of API calls is equal to the number of total pages in the responses.
- A few fields of the response json that may not be important have not been considered in this sample.
- Please refer the documentation for the complete response structure.
'''


if __name__ == "__main__":

    api_endpoint = "https://api.helpshift.com/v1/" + DOMAIN + "/issues?page-size=1000&"

    with open(ISSUES_FILE_LOC, 'wb') as issues_file, open(MESSAGES_FILE_LOC, 'wb') as messages_file:

        issue_fieldnames = {'assignee_name', 'domain', 'title', 'tags', 'app_id', 'id', 'state', 'changed_at'}
        message_fieldnames = {'issue_id', 'body', 'author', 'attachment'}
        issue_writer = csv.DictWriter(issues_file, fieldnames=issue_fieldnames, extrasaction='ignore', restval='')
        message_writer = csv.DictWriter(messages_file, fieldnames=message_fieldnames, extrasaction='ignore', restval='')
        issue_writer.writeheader()
        message_writer.writeheader()
        current_page = 0

        while True:

            current_page = current_page + 1
            api_endpoint_with_pagination = api_endpoint + 'page=' + str(current_page)
            response = requests.get(api_endpoint_with_pagination, auth=(API_KEY, ""))

            if response.status_code != 200:
                print "Something went wrong: " + str(response.json())
                exit(1)

            resp = response.json()
            if resp['total-pages'] < current_page:
                break

            for issue in resp['issues']:
                issue_writer.writerow(dict(issue,
                                           state=issue['state_data']['state'],
                                           tags=', '.join(issue['tags']),
                                           changed_at=issue['state_data']['changed_at']))

                for message in issue['messages']:
                    message_writer.writerow(dict(issue_id=issue['id'],
                                                 body=message['body'],
                                                 author=message['author']['name'],
                                                 attachment=message.get('attachment', {}).get('file_name')))
