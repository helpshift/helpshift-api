# Python Helpshift API Sample Code

This projects contains the sample code for using Helpshift API to create an issue,
add message with attachment, and export API response to csv files in Python.

## Setup and Usage Instructions

1. To use the sample code, Python 2 should be installed.

2. Install the project dependencies using below command.
   ```
   pip install -r requirements.txt
   ```

3. Retrieve your [Helsphift API key](https://success.helpshift.com/a/success-center/?p=web&s=premium-features&f=managing-your-api-keys).

4. Replace DOMAIN, API_KEY, ATTACHMENT_FILE_PATH, TEST_PAYLOAD, ISSUE_FILE_LOCATION and MESSAGES_FILE_LOCATION, as required, in
   [create_issue_with_attachment.py](./create_issue_with_attachment.py) ,
   [add_message_with_attachment.py](./add_message_with_attachment.py) and
   [export_issues_to_csv.py](./export_issues_to_csv.py) with actual values.
   - Note: Use GET /apps API to retrieve app_id. Refer to [Helsphift API documentation](https://apidocs.helpshift.com/)
   for API parameters.

5. Create issue by using following command and note the issue_id.
   ```
   python create_issue_with_attachment.py
   ```

6. Add message to issue using following command. This script accepts an issue_id.
   ```
   python add_message_with_attachment.py <ISSUE_ID>
   ```

7. Export all issues and messages created in the last given number of days into separate files using following command.
   ```
   python export_issues_to_csv.py <NO_OF_DAYS>
   ```

8. Backfill Custom Issue Fields from Metadata.
   ```
   python backfill_custom_issue_fields.py
   ```
