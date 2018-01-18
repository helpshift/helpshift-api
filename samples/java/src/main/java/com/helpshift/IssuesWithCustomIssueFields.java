package com.helpshift;

import com.mashape.unirest.http.HttpResponse;
import com.mashape.unirest.http.JsonNode;
import com.mashape.unirest.http.Unirest;
import com.mashape.unirest.http.exceptions.UnirestException;
import org.json.simple.JSONArray;
import org.json.simple.parser.JSONParser;
import org.json.simple.JSONObject;
import org.json.simple.parser.ParseException;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.Scanner;

/******

 * Notes:

 1. The payloads used here assume that the following custom issue fields are present in the system.

        Name of field       Type of field

        1. item             dropdown
        2. gift_wrapped     checkbox
        3. order_id         singleline
        4. billing_name     singleline
        5. billing_address  multiline
        6. order_date       date
        7. quantity         number
        8. customer_id      number

 2.
 - Custom issue fields (CIFs) of all types have been considered in this example.
 - This program allows a user to create and retrieve issues with CIFs.
 - Create issues option will create issues having different values for each CIF.
 - Please refer json file "src/main/resources/cif_payloads" for CIFs that are used for these issues.
 - Get issues will retrieve issues depending on a variety of filter conditions.
 - Please refer json file "src/main/resources/cif_filters" for details.
 - All possible conditions on all types of CIFs have been used here.
 - Please refer the API documentation for further details on how to use CIFs while creating or retrieving an issue.

 ******/


public class IssuesWithCustomIssueFields {

    private String base_url = "https://api.helpshift.com/v1/";

    private void CreateIssues(String domain, String api_key) {

        String issues_endpoint = base_url + domain + "/issues/";

        try {

            JSONParser parser = new JSONParser();
            Object obj = parser.parse(new FileReader("src/main/resources/cif_payloads"));
            JSONArray cif_payloads = (JSONArray) obj;

            for (Object cif_payload : cif_payloads) {

                HttpResponse<JsonNode> response = Unirest.post(issues_endpoint)
                        .basicAuth(api_key, "")
                        .header("accept", "application/json")
                        .field("email", "test@mail.com")
                        .field("message-body", "Custom Issue Fields Demo.")
                        .field("title", "Issue with random custom issue fields")
                        .field("custom_fields", cif_payload)
                        .asJson();

                System.out.println("Issue created with custom fields: " + response.getBody());
            }
        } catch (FileNotFoundException fnf) {
            System.err.println("CIF payloads json file not found:" + fnf.getMessage());
        } catch (UnirestException ue) {
            System.err.println("Error making API request:" + ue.getMessage());
            ue.printStackTrace();
        } catch (ParseException pe) {
            System.err.println("Failed parsing JSON file: " + pe.getMessage());
            pe.printStackTrace();
        } catch (IOException ioe) {
            ioe.printStackTrace();
        }
    }

    private void GetIssues(String domain, String api_key) {

        try {

            JSONParser parser = new JSONParser();
            Object obj = parser.parse(new FileReader("src/main/resources/cif_filters"));
            JSONArray cif_filters = (JSONArray) obj;
            Scanner input = new Scanner(System.in);
            String issues_endpoint = base_url + domain + "/issues/";

            while (true) {

                // Display filter options

                System.out.println("\n\nAvailable filters:");
                int counter = 0;
                for (Object cif_obj : cif_filters) {
                    JSONObject cif_filter = (JSONObject) cif_obj;
                    System.out.println(++counter + ". " + cif_filter.get("description"));
                }
                System.out.println("Enter the filter number to filter or any other number to quit: ");
                int choice = Integer.parseInt(input.nextLine());
                if (choice < 1 || choice > counter)
                    return;

                // Do the GET call

                JSONObject filter_condition = (JSONObject) cif_filters.get(--choice);
                HttpResponse<JsonNode> response = Unirest.get(issues_endpoint)
                        .basicAuth(api_key, "")
                        .header("accept", "application/json")
                        .queryString("custom_fields", filter_condition.get("query"))
                        .queryString("state", "new")
                        .queryString("includes", "[\"custom_fields\"]")
                        .asJson();

                // Handle the response

                org.json.JSONObject resp_body = response.getBody().getObject();

                if (response.getStatus() != 200) {
                    System.out.println("Something went wrong for condition: " + filter_condition.get("description") +
                            "\nResponse: " + resp_body);
                    System.exit(1);
                }

                System.out.println("Condition:" + filter_condition.get("description") +
                        "\nNumber of issues: " + resp_body.get("total-hits") +
                        "\nIssues: " + resp_body.get("issues"));
            }

        } catch (FileNotFoundException fnf) {
            System.err.println("CIF filters json file not found:" + fnf.getMessage());
        } catch (UnirestException ue) {
            System.err.println("Error making API request:" + ue.getMessage());
            ue.printStackTrace();
        } catch (ParseException pe) {
            System.err.println("Failed parsing JSON file: " + pe.getMessage());
            pe.printStackTrace();
        } catch (IOException ioe) {
            ioe.printStackTrace();
        } catch (NumberFormatException nfe) {
            System.err.println("Wrong choice given: " + nfe.getMessage());
        }
    }

    private void MenuDriven(String domain, String api_key) {

        Scanner input = new Scanner(System.in);
        while (true) {
            System.out.print("\n\nType of Action:\t1. Create Issues\t2. Retrieve Issues\t3. Exit Program" +
                    "\nPlease enter your choice: ");
            try {
                int choice = Integer.parseInt(input.nextLine());
                switch (choice) {
                    case 1:
                        CreateIssues(domain, api_key);
                        break;
                    case 2:
                        GetIssues(domain, api_key);
                        break;
                    case 3:
                        return;
                    case 4:
                        System.out.println("Wrong choice.");
                }
            } catch (Exception e) {
                System.err.println("Exception: " + e.getMessage());
                e.printStackTrace();
            }
        }
    }

    public static void main(String args[]) {
        String domain = "<DOMAIN>";
        String api_key = "<API_KEY>";
        IssuesWithCustomIssueFields obj = new IssuesWithCustomIssueFields();
        obj.MenuDriven(domain, api_key);
    }
}
