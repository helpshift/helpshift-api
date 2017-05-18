(defproject api-sample-code "0.1.0-SNAPSHOT"
  :description "This project provides sample code for using Helpshift API."
  :url "http://example.com/FIXME"
  :license {:name "Proprietary"}
  :dependencies [[org.clojure/clojure "1.8.0"]
                 [http-kit "2.2.0"]
                 [com.novemberain/pantomime "2.9.0"]
                 [cheshire "5.7.1"]
                 [http-kit.fake "0.2.1"]]
  :source-path "src"
  :manifest {"Project-Name" ~#(:name %)
             "Project-Version" ~#(:version %)
             "Build-Date" ~(str (java.util.Date.))}
  :main ^:skip-aot api-sample-code.create-issue-with-attachment
  :target-path "target/%s"
  :profiles {:uberjar {:aot :all}})
