(ns api-sample-code.create-issue-with-attachment
  (:require [org.httpkit.client :as http]
            [cheshire.core :as json]
            [pantomime.mime :refer [mime-type-of]]
            [clojure.string :as cs]))


(def HS-API-ENDPOINT "https://api.helpshift.com/v1/")


(defn construct-multipart-request-data
  "Constructs a multipart body given a data map containing attachment key.
  Input: {:email \"test@mail.com\"
          :message-body \"Create issue\"
          :attachment \"file-url\"}
  Output: [{:name \"email\" :content \"test@mail.com\"}
           {:name \"message-body\" :content \"Create issue\"}
           {:name \"attachment\" :filename \"file-name\" :content-type \"file-type\" :content \"java.io.File object\"}]"
  [data]
  (let [multipart-data (mapv (fn [k]
                               {:name (name k)
                                :content (k data)})
                             (keys (dissoc data :attachment )))
        attachment-file-path (:attachment data)
        multipart-data-with-attachment (conj multipart-data
                                             {:name "attachment"
                                              :filename (last (cs/split (:attachment data) #"/"))
                                              :content (clojure.java.io/file attachment-file-path)
                                              :content-type (mime-type-of attachment-file-path)})]
    multipart-data-with-attachment))


(defn create-issue
  "Create issue given a domain name, api key, issue data map."
  [domain api-key issue-data]
  (let [multipart-request-data (construct-multipart-request-data issue-data)
        create-issue-api-endpoint (str HS-API-ENDPOINT
                                       domain
                                       "/issues")
        api-response @(http/post create-issue-api-endpoint
                                 {:basic-auth api-key
                                  :multipart multipart-request-data})]
    (json/parse-string (:body api-response) true)))


(comment
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
                 :attachment "resources/img_01.jpg"}))
