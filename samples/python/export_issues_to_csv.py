import requests
import csv
import sys
import datetime


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
- To limit the total size of response, the program takes number of days N as input.
  Issues created in the last N days will be fetched. To get ALL issues, remove the parameter 'created_since'.
- A few fields of the response json that may not be important have not been considered in this sample.
- Please refer the documentation for the complete response structure.
'''

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print "Please enter number of days N. Issues created in the last N days will be retrieved.\n" \
              "Usage: python export_issues_to_csv.py <NO OF DAYS>"
        exit(1)

    timestamp_in_ms = 0

    try:
        N = int(sys.argv[1])
        timestamp_in_secs = (datetime.date.today() - datetime.timedelta(days=N)).strftime("%s")
        timestamp_in_ms = long(timestamp_in_secs) * 1000
    except ValueError as ve:
        print "Wrong value given for number of days = " + sys.argv[1]
        exit(2)

    api_endpoint = "https://api.helpshift.com/v1/" + DOMAIN + "/issues?page-size=1000&created_since=" + \
                   str(timestamp_in_ms) + "&"

    '''
    Example API with some filters:
        sort-by creation-time, issue state is new, response includes meta
            "https://api.helpshift.com/v1/" + DOMAIN +
            "/issues?sort-by=creation-time&state=%5B%22new%22%5D&includes=%5B%22meta%22%5D&page-size=1000&"

    Please refer the documentation to add filters to GET /issues API as required.
    '''

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
                print ("Export completed. Total number of API calls: " + str(current_page - 1))
                break

            for issue in resp['issues']:
                try:
                    '''
                    Certain string fields that may contain non-ASCII characters
                    have to be explicitly encoded for csv writer
                    '''
                    assignee_name = issue['assignee_name'].encode("utf-8") if issue['assignee_name'] else ""
                    issue_writer.writerow(dict(issue,
                                               assignee_name=assignee_name,
                                               title=issue.get('title',"").encode("utf-8"),
                                               state=issue['state_data']['state'],
                                               tags=', '.join(issue['tags']),
                                               changed_at=issue['state_data']['changed_at']))

                    for message in issue['messages']:
                        message_writer.writerow(dict(issue_id=issue['id'],
                                                     body=message['body'].encode("utf-8"),
                                                     author=message['author']['name'].encode("utf-8"),
                                                     attachment=message.get('attachment', {}).get('file_name')))
                except Exception as ee:
                    print ("Exception for Issue ID: " + str(issue['id']))
                    print (ee)
                    pass
