package com.helpshift;

import com.mashape.unirest.http.HttpResponse;
import com.mashape.unirest.http.Unirest;
import com.mashape.unirest.http.exceptions.UnirestException;
import org.json.*;
import java.io.*;
import java.util.Calendar;
import org.apache.commons.lang3.StringUtils;


public class ExportIssuesToCsv {


    public JSONObject GetIssues (String domain, String api_key, int page, long created_since) {

        try {
            String api_endpoint = "https://api.helpshift.com/v1/" + domain + "/issues?page-size=1000&created_since=" +
                    created_since + "&page=" + page;

            /*
            * Example API with some filters:
                sort-by creation-time, issue state is new, response includes meta
                "https://api.helpshift.com/v1/" + domain +
                "/issues?sort-by=creation-time&state=%5B%22new%22%5D&includes=%5B%22meta%22%5D&page-size=1000&"

            * Please refer the documentation to add filters to GET /issues API as required.
            * */

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

    public void getAndSaveToCsv(String domain, String api_key, String issues_file_loc, String messages_file_loc,
                                long created_since) {

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
                JSONObject resp = GetIssues(domain, api_key, current_page, created_since);
                if (resp.getInt("total-pages") < current_page) {
                    System.out.println("Export completed. Total number of API calls: " + (current_page - 1));
                    break;
                }

                /*
                * The response will contain issue details in nested json structure.
                * Below code will flatten the structure by extracting fields as required.
                * It will also flatten the tags array into a string for better readability.
                * The json keys are the names of columns in the output issue CSV file.
                * */

                JSONArray issues = resp.getJSONArray("issues");
                for (int i = 0 ; i < issues.length() ; i++) {

                    JSONObject issue = issues.getJSONObject(i);
                    JSONObject state_data = issue.getJSONObject("state_data");

                    JSONArray tags_array = issue.getJSONArray("tags");
                    StringBuilder tags = new StringBuilder("");
                    for (int k = 0 ; k < tags_array.length() ; k++) {
                        tags = tags.append(tags_array.getString(k)).append(",");
                    }
                    if (tags.length() > 0)
                        tags.deleteCharAt(tags.length() - 1);

                    issues.getJSONObject(i).put("state",  state_data.get("state"));
                    issues.getJSONObject(i).put("changed_at",  state_data.get("changed_at"));
                    issues.getJSONObject(i).put("tags", tags);

                    /*
                    * Destructuring message json and renaming keys to columns of output message CSV file.
                    * */

                    JSONArray messages = issue.getJSONArray("messages");
                    for (int j = 0 ; j < messages.length() ; j++) {
                        JSONObject message = messages.getJSONObject(j);
                        messages.getJSONObject(j).put("issue_id", issue.get("id"));
                        messages.getJSONObject(j).put("author", message.getJSONObject("author").get("name"));
                        if (message.has("attachment")) {
                            messages.getJSONObject(j).put("attachment", message.getJSONObject("attachment").get("file_name"));
                        }
                    }

                    /*
                    * CDL provides support for converting between JSON and comma delimited lists.
                    * Given the column names and array of json objects with columns as keys,
                    * it returns comma delimited text mapped to columns.
                    * For more details, refer https://github.com/vogella/org.json/blob/master/src/org/json/CDL.java
                    * */

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
        - To limit the total size of response, the program takes number of days N as input.
          Issues created in the last N days will be fetched. To get ALL issues, remove the parameter 'created_since'.
        - A few fields of the response json that may not be important have not been considered in this sample.
        - Please refer the documentation for the complete response structure.
         */

        if (args.length != 1) {
            System.out.println("Please enter number of days N. Issues created in the last N days will be retrieved.\n" +
                    "Usage: java -cp <PATH TO JAR> com.helpshift.ExportIssuesToCsv <NO OF DAYS>");
            System.exit(1);
        }

        Calendar c = Calendar.getInstance();
        try {
            int no_of_days = Integer.parseInt(args[0]);
            c.add(Calendar.DATE, (-1 * no_of_days));
        } catch (Exception e) {
            System.out.println("Wrong value given for number of days = " + args[0]);
            System.exit(2);
        }
        long created_since = c.getTimeInMillis();

        String domain = "<DOMAIN>";
        String api_key = "<API_KEY>";
        String issues_file_location = "<ISSUES_FILE_LOCATION>/issues.csv";
        String messages_file_location = "<MESSAGES_FILE_LOCATION>/messages.csv";

        ExportIssuesToCsv exportIssuesToCsv = new ExportIssuesToCsv();
        exportIssuesToCsv.getAndSaveToCsv(domain, api_key, issues_file_location, messages_file_location, created_since);
    }
}
