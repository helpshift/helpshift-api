# Clojure Helpshift API Sample Code

This project contains the sample code for using Helpshift API to create issue and add message with attachment in Clojure.

## Setup and Usage Instructions

1. To run this project, [Leiningen](https://leiningen.org/) needs to be installed.
   Follow instructions on [this](https://leiningen.org/) page to setup Leiningen.

2. Download the project dependencies and compile the project using following command.
   ```
   lein do clean, deps, compile
   ```

3. Now run the project using following command from root directory of the project.
   ```
   lein repl
   ```

4. Retrieve your [Helsphift API key](https://success.helpshift.com/a/success-center/?p=web&s=premium-features&f=managing-your-api-keys).

5. Create issue with attachment using following function call and note the issue id returned by function.
   This function accepts three parameters:
   - Domain name in Helpshift.
   - API key.
   - Issue data map (this will be used to create issue). Replace the sample attachment's path with the path of an attachment you want to upload.
   - Note: Use GET /apps API to retrieve app_id. Refer to [Helsphift API documentation](https://apidocs.helpshift.com/)
   for API parameters.

   ```
   (require 'api-sample-code.create-issue-with-attachment)
   (in-ns 'api-sample-code.create-issue-with-attachment)
   (create-issue "<DOMAIN>"
                 "<API-KEY>"
                 {:message-body "Test message"
                  :email "Test@mail.com"
                  :title "Issue title"
                  :tags (json/generate-string ["test"])
                  :meta (json/generate-string {:test 1})
                  :author-name "test-user"
                  :platform-type "web"
                  :app-id "<APP-ID>"
                  :attachment "resources/img_01.jpg"})
   ```

6. Add message with attachment to previously created issue.
   This function accepts four parameters:
   - Domain name in Helpshift.
   - API key.
   - Issue id (Id of the issue to which you want to add this message.)
   - Message data map (this will be used to add message). Replace the sample attachment's path with the path of an attachment you want to upload.

   ```
   (require 'api-sample-code.add-message-with-attachment)
   (in-ns 'api-sample-code.add-message-with-attachment)
   (add-message "<DOMAIN>"
                "<API-KEY>"
                "<ISSUE_ID>"
                {:message-body "Add message test"
                 :message-type "Text"
                 :attachment "resources/img_01.jpg"})
   ```

7. This project also contains unit tests for the above functions. The tests can be run by:
   ```
   lein test
   ```