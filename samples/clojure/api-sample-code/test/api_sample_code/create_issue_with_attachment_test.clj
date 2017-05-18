(ns api-sample-code.create-issue-with-attachment-test
  (:require [clojure.test :refer :all]
            [org.httpkit.client :as http]
            [cheshire.core :as json]
            [api-sample-code.create-issue-with-attachment :as create-issue])
  (:use org.httpkit.fake))


(deftest create-issue-test
  (testing "Create Issue with attachment test."
    (with-fake-http [{:url "https://api.helpshift.com/v1/random/issues" :method :post}
                     {:status 201 :body (json/generate-string {:created_at 1494306123899
                                                               :id "5000"
                                                               :title "Test issue"
                                                               :tags ["foo" "bar"]
                                                               :meta {"test" "1"}
                                                               :attachment {:size 116552
                                                                            :content_type "image/jpeg"
                                                                            :file_name "img_01.jpg"
                                                                            :url "test-url.jpg"}})}]
      (let [issue-data (create-issue/create-issue "random"
                                                  "random-key"
                                                  {:message-body "Test issue"
                                                   :email "test@mail.com"
                                                   :title "Test issue"
                                                   :tags (json/generate-string ["foo" "bar"])
                                                   :meta (json/generate-string {:test "1"})
                                                   :author-name "Test-user"
                                                   :platform-type "web"
                                                   :app-id "random_app_123"
                                                   :attachment "resources/img_01.jpg"})]
        (is (= (keys issue-data)
               [:created_at :id :title :tags :meta :attachment]))))))
