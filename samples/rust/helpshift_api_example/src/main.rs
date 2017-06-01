extern crate curl;
#[macro_use]
extern crate serde_json;
extern crate base64;

use std::path::Path;

use curl::easy::{Easy, List, Form};
use serde_json::{Value};
use base64::{encode};

fn main() {
    // Change the values of the following API request parameters as necessary.
    let domain = "<DOMAIN>"; // Replace this with your Helpshift domain.
    let api_key = "<API-KEY>"; // Replace this with your REST API Key
    let file_path = "<PATH-TO-ATTACHMENT-FILE>"; // Replace this with the patch to the attachment
    let email = b"<EMAIL>";
    let file_type = "image/png";
    let title = b" Test Issue title";
    let message_body = b"Test message body";

    let tags_json = json!(["premium", "testing"]);
    let meta_json = json!({"one" : 1,
                           "two"  : 2});

    let mut handle = Easy::new();

    let api_prefix_url = "https://api.helpshift.com/v1";
    let create_issue_url = format!("{}/{}/issues/", api_prefix_url, domain);
    handle.url(create_issue_url.as_str()).unwrap();

    let mut headers = List::new();

    let basic_auth_header = format!("Authorization: Basic {}", encode(api_key));
    headers.append(basic_auth_header.as_str()).unwrap();
    handle.http_headers(headers).unwrap();

    let mut form = Form::new();

    form.part("title").contents(title).add();
    form.part("message-body").contents(message_body).add();
    form.part("email").contents(email).add();
    form.part("tags").contents(tags_json.to_string().as_bytes()).add();
    form.part("meta").contents(meta_json.to_string().as_bytes()).add();
    form.part("attachment").content_type(file_type).file(Path::new(file_path)).add();

    handle.httppost(form);
    handle.perform().unwrap();

    let mut response_buffer = Vec::new();
    {
        let mut transfer = handle.transfer();
        transfer.write_function(|new_data| {
            response_buffer.extend_from_slice(new_data);
            Ok(new_data.len())
        }).unwrap();
        transfer.perform().unwrap();
    }
    let response = String::from_utf8_lossy(response_buffer.as_slice());

    let resp_json: Value = serde_json::from_str(&response).unwrap();
    println!("Created Issue ID: {}", resp_json["id"]);
}
