(ns api-sample-code.add-message-with-attachment-test
  (:require [clojure.test :refer :all]
            [org.httpkit.client :as http]
            [cheshire.core :as json]
            [api-sample-code.add-message-with-attachment :as add-message])
  (:use org.httpkit.fake))


(deftest add-message-test
  (testing "Add message with attachment test."
    (with-fake-http [{:url "https://api.helpshift.com/v1/random/issues/1/messages" :method :post}
                     {:status 201 :body (json/generate-string {:added-message {:body "Test issue"
                                                                               :type "Text"
                                                                               :attachment {:size 116552
                                                                                            :content_type "image/jpeg"
                                                                                            :file_name "img_01.jpg"
                                                                                            :url "test-url.jpg"}}})}]
      (let [issue-data (add-message/add-message "random"
                                                "random-key"
                                                1
                                                {:message-body "Test issue"
                                                 :message-type "Text"
                                                 :attachment "resources/img_01.jpg"})]
        (is (= (keys issue-data)
               [:added-message]))))))
