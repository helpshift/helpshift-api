package com.helpshift;

import com.mashape.unirest.http.HttpResponse;
import com.mashape.unirest.http.Unirest;
import com.mashape.unirest.http.exceptions.UnirestException;
import org.apache.http.entity.ContentType;
import org.apache.http.entity.mime.content.InputStreamBody;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.InputStream;
import java.net.URLConnection;

public class AddMessageWithAttachment {
    String message_body;
    String message_type;
    String attachment_url;

    public AddMessageWithAttachment(String message_body,
                   String message_type,
                   String attachment_url) {
        this.message_body = message_body;
        this.message_type = message_type;
        this.attachment_url = attachment_url;
    }

    public void addMessage(String api_endpoint, String api_key) {
        String attachment_file_name = this.attachment_url.substring(this.attachment_url.lastIndexOf("/") + 1);
        try {
            HttpResponse<String> response = Unirest.post(api_endpoint)
                    .basicAuth(api_key, "")
                    .field("message-body", this.message_body)
                    .field("message-type", this.message_type)
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
        } catch (Exception exception) {
            System.err.println(exception.getMessage());
            exception.printStackTrace();
        }
    }

    public static void main(String[] args) {
        if (args.length != 1){
            System.out.println("Please pass issue-id as parameter.");
            System.exit(1);
        }
        String domain = "<DOMAIN>";
        String issue_id = args[0];
        String api_endpoint = "https://api.helpshift.com/v1/" + domain + "/issues/" + issue_id + "/messages";
        String api_key = "<API-KEY>";

        AddMessageWithAttachment sample_message = new AddMessageWithAttachment("Test message",
                "Text",
                "src/main/resources/img_01.jpg");

        sample_message.addMessage(api_endpoint,
                api_key);
    }
}
