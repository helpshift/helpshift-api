# Java Helpshift API Sample Code

This project contains the sample code for using Helpshift API to create issue,
add message with attachment and export API response to csv files in Java.

## Setup and Usage Instructions

1. To use the sample code, [JDK 1.7 or higher](http://www.oracle.com/technetwork/java/javase/downloads/jdk7-downloads-1880260.html)
   and [Maven](https://maven.apache.org/) is required.

2. Retrieve your [Helsphift API key](https://success.helpshift.com/a/success-center/?p=web&s=premium-features&f=managing-your-api-keys).

3. Replace the placeholder values in [CreateIssueWithAttachment.java](src/main/java/com/helpshift/CreateIssueWithAttachment.java),
    [AddMessageWithAttachment](src/main/java/com/helpshift/AddMessageWithAttachment.java) and
    [ExportIssuesToCsv](src/main/java/com/helpshift/ExportIssuesToCsv.java).
   - Replace the sample attachment's path with the path of an attachment you want to upload.
   - Replace the paths for issue and message csv files.
   - Note: Use GET /apps API to retrieve app_id. Refer to [Helsphift API documentation](https://apidocs.helpshift.com/)
   for API parameters.

4. Run mvn package. This will generate a self-contained jar with all dependencies included.
   ```
   mvn package
   ```

5. Create issue using following command and note the issue-id.
   ```
   java -cp target/api-sample-code-1.0.0-jar-with-dependencies.jar com.helpshift.CreateIssueWithAttachment
   ```

6. Add message to issue created in previous step using following command.
   ```
   java -cp target/api-sample-code-1.0.0-jar-with-dependencies.jar com.helpshift.AddMessageWithAttachment <ISSUE_ID>
   ```

7. Export all issues and messages to CSV files using following command.
      ```
      java -cp target/api-sample-code-1.0.0-jar-with-dependencies.jar com.helpshift.ExportIssuesToCsv
      ```