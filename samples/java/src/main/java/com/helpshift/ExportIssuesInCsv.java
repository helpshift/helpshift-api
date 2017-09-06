package com.helpshift;

import com.mashape.unirest.http.HttpResponse;
import com.mashape.unirest.http.Unirest;
import com.mashape.unirest.http.exceptions.UnirestException;
import org.json.*;
import java.io.*;
import org.apache.commons.lang3.StringUtils;


public class ExportIssuesInCsv {


    public JSONObject GetIssues (String domain, String api_key, int page) {

        try {
            String api_endpoint = "https://api.helpshift.com/v1/" + domain + "/issues?page-size=1000&page=" + page;

            HttpResponse<String> response = Unirest.get(api_endpoint)
                    .basicAuth(api_key, "")
                    .asString();

            JSONObject resp_body = new JSONObject(response.getBody());

            if (response.getStatus() != 200) {
                System.out.println ("Something went wrong: " + resp_body);
                System.exit(1);
            }

            return resp_body;

        } catch (UnirestException exception) {
            System.err.println("Exception in making API request: " + exception.getMessage());
            exception.printStackTrace();
            return null;
        }
    }

    public void getAndSaveToCsv(String domain, String api_key, String issues_file_loc, String messages_file_loc) {

        try {
            FileWriter issues_file = new FileWriter(issues_file_loc);
            BufferedWriter bw = new BufferedWriter(issues_file);
            PrintWriter pw = new PrintWriter(bw);
            FileWriter messages_file = new FileWriter(messages_file_loc);
            BufferedWriter bwm = new BufferedWriter(messages_file);
            PrintWriter pwm = new PrintWriter(bwm);

            int current_page = 0;
            String [] issue_field_names = {"domain", "id", "title", "app_id", "assignee_name", "tags", "state", "changed_at"};
            JSONArray issue_fields = new JSONArray(issue_field_names);
            String [] message_field_names = {"issue_id", "body", "author", "attachment"};
            JSONArray message_fields = new JSONArray(message_field_names);

            // Creating CSV file headers
            pw.println(StringUtils.join(issue_field_names,','));
            pwm.println(StringUtils.join(message_field_names,','));

            while (true) {
                current_page++;
                JSONObject resp = GetIssues(domain, api_key, current_page);
                if (resp.getInt("total-pages") < current_page) {
                    break;
                }

                // Rename issue fields in response json to CSV column names
                JSONArray issues = resp.getJSONArray("issues");
                for (int i = 0 ; i < issues.length() ; i++) {
                    JSONObject issue = issues.getJSONObject(i);
                    JSONObject state_data = issue.getJSONObject("state_data");
                    issues.getJSONObject(i).put("state",  state_data.get("state"));
                    issues.getJSONObject(i).put("changed_at",  state_data.get("changed_at"));

                    // Rename message fields for each issue
                    JSONArray messages = issue.getJSONArray("messages");
                    for (int j = 0 ; j < messages.length() ; j++) {
                        JSONObject message = messages.getJSONObject(j);
                        messages.getJSONObject(j).put("issue_id", issue.get("id"));
                        messages.getJSONObject(j).put("author", message.getJSONObject("author").get("name"));
                        if (message.has("attachment")) {
                            messages.getJSONObject(j).put("attachment", message.getJSONObject("attachment").get("file_name"));
                        }
                    }
                    pwm.print(CDL.toString(message_fields, messages));
                }
                pw.print(CDL.toString(issue_fields, issues));
            }
            pw.flush();
            pwm.flush();
        }
        catch (IOException e) {
            System.err.println("Exception while writing to file: " + e.getMessage());
            e.printStackTrace();
        }
        catch (Exception e) {
            System.err.println("Unexpected Exception: " + e.getMessage());
            e.printStackTrace();
        }
        return;
    }

    public static void main(String args[]) {
        /*
        * POINTS TO NOTE:
        - Messages are exported to a different file for ease of access.
        - Each message row will have its corresponding issue id.
        - The API will fetch 1000 (maximum allowed) issues per call, as specified in the 'api_endpoint' above.
        - Total number of API calls is equal to the number of total pages in the responses.
        - A few fields of the response json that may not be important have not been considered in this sample.
        - Please refer the documentation for the complete response structure.
         */
        String domain = "<DOMAIN>";
        String api_key = "<API_KEY>";
        String issues_file_location = "<ISSUES_FILE_LOCATION>/issues.csv";
        String messages_file_location = "<MESSAGES_FILE_LOCATION>/messages.csv";

        ExportIssuesInCsv exportIssuesInCsv = new ExportIssuesInCsv();
        exportIssuesInCsv.getAndSaveToCsv(domain, api_key, issues_file_location, messages_file_location);
    }
}
