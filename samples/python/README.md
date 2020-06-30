# Python Helpshift API Sample Code

This projects contains the sample code for using Helpshift API to create an issue,
add message with attachment to an issue, create and retrieve issues with custom issue fields,
and export API response to csv files in Python.

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
   - Note: Use GET /apps API to retrieve app_id. Refer to [Helsphift API documentation](https://apidocs.helpshift.com/) for API parameters.

5. Please refer [custom_issue_field_payloads.py](./custom_issue_field_payloads.py) for a variety of payload structures
   to create and retrieve issues with custom issue fields.

6. Create issue by using following command and note the issue_id.
   ```
   python create_issue_with_attachment.py
   ```

7. Add message to issue using following command. This script accepts an issue_id.
   ```
   python add_message_with_attachment.py <ISSUE_ID>
   ```

8. Create issues with custom issue fields and retrieve them using conditional filters.
   ```
   python issues_with_custom_issue_fields.py
   ```


9. Export all issues and messages created in the last given number of days into separate files using following command.
   ```
   python export_issues_to_csv.py <NO_OF_DAYS>
   ```
8. Backfill Custom Issue Fields from Metadata.
   ```
   python backfill_custom_issue_fields.py
   ```

9. Update Custom Issue Fields of multiple Issues.
   ```
   python update_multiple_issues.py
   ```

10. Update multiple issues using Bulk Edit API
   ```
   python bulk_edit_issues.py
   ```
