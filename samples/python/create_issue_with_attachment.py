import json
import requests
import mimetypes


DOMAIN = "<DOMAIN>"
API_KEY = "<API_KEY>"
ATTACHMENT_FILE_PATH = "<ATTACHMENT FILE PATH>"
TEST_PAYLOAD = {"email": "test@mail.com",
                "message-body": "Attachments Demo",
                "title": "Test issue title",
                "tags": json.dumps(["foo"]),
                "meta": json.dumps({"test": 1}),
                "author-name": "Test author",
                "platform-type": "web",
                "app-id": "random_app_20140423095931205-caae76e3be13ef6"}


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
    api_endpoint = 'https://api.helpshift.com/v1/{0}/issues'.format(DOMAIN)
    attachment_object = construct_attachment_object(ATTACHMENT_FILE_PATH)
    make_api_call(api_endpoint,
                  API_KEY,
                  TEST_PAYLOAD,
                  attachment_object)
