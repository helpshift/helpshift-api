import sys
import requests
import mimetypes


DOMAIN = "<DOMAIN>"
API_KEY = "<API_KEY>"
ATTACHMENT_FILE_PATH = "<ATTACHMENT FILE PATH>"
TEST_PAYLOAD = {"message-body": "Add message with attachment",
                "message-type": "Text"}


def construct_attachment_object(attachment_url):
    file_name = attachment_url.split("/")[-1]
    file_type, encoding = mimetypes.guess_type(attachment_url)
    return {"attachment": (file_name,
                           open(attachment_url, "rb"),
                           file_type)}


def make_api_call(api_endpoint, api_key, payload, attachment={}):
    response = requests.post(api_endpoint,
                             auth=(api_key, ""),
                             data=payload,
                             files=attachment)
    print "API response status {0}".format(response.status_code)
    print "API response {0}".format(response.json())


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Please pass issue_id as second argument to script."
        print "Usage: python add_message_with_attachment.py <ISSUE ID>"
        exit(1)
    issue_id = sys.argv[1]
    api_endpoint = "https://api.helpshift.com/v1/{0}/issues/{1}/messages".format(DOMAIN, issue_id)
    attachment_object = construct_attachment_object(ATTACHMENT_FILE_PATH)
    make_api_call(api_endpoint,
                  API_KEY,
                  TEST_PAYLOAD,
                  attachment_object)
