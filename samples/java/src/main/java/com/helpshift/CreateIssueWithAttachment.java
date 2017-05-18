package com.helpshift;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.net.URLConnection;

import com.mashape.unirest.http.HttpResponse;
import com.mashape.unirest.http.Unirest;
import com.mashape.unirest.http.exceptions.UnirestException;
import org.apache.http.entity.ContentType;

public class CreateIssueWithAttachment {
    String message_body;
    String email;
    String title;
    String author_name;
    String platform_type;
    String app_id;
    String attachment_url;
    String tags;
    String meta;

    public CreateIssueWithAttachment(String message_body,
                 String email,
                 String title,
                 String author_name,
                 String platform_type,
                 String app_id,
                 String tags,
                 String meta,
                 String attachment_url) {
        this.message_body = message_body;
        this.email = email;
        this.title = title;
        this.author_name = author_name;
        this.platform_type = platform_type;
        this.app_id = app_id;
        this.tags = tags;
        this.meta = meta;
        this.attachment_url = attachment_url;
    }

    public void createIssue(String api_endpoint, String api_key) {
        String attachment_file_name = this.attachment_url.substring(this.attachment_url.lastIndexOf("/") + 1);

        try {
            HttpResponse<String> response = Unirest.post(api_endpoint)
                    .basicAuth(api_key, "")
                    .field("email", this.email)
                    .field("message-body", this.message_body)
                    .field("title", this.title)
                    .field("platform-type", this.platform_type)
                    .field("app-id", this.app_id)
                    .field("meta", this.meta)
                    .field("tags", this.tags)
                    .field("attachment", new FileInputStream(new File(this.attachment_url)),
                            ContentType.create(URLConnection.guessContentTypeFromName(this.attachment_url)),
                            attachment_file_name)
                    .asString();

            System.out.println("Response status:" + response.getStatus());
            System.out.println("Response body:" + response.getBody());
        } catch (UnirestException exception) {
            System.err.println("Error making API request:" + exception.getMessage());
            exception.printStackTrace();
        } catch (FileNotFoundException exception) {
            System.err.println(exception.getMessage());
            exception.printStackTrace();
        }
    }

    public static void main(String[] args) {
        String domain = "<DOMAIN>";
        String api_endpoint = "https://api.helpshift.com/v1/" + domain + "/issues/";
        String api_key = "<API-KEY>";

        CreateIssueWithAttachment sample_issue = new CreateIssueWithAttachment("Test Issue",
                "test@mail.com",
                "Issue title",
                "Author Name",
                "web",
                "<APP-ID>",
                "[\"foo\"]",
                "{\"test\": 1}",
                "src/main/resources/img_01.jpg");

        sample_issue.createIssue(api_endpoint, api_key);
    }
}