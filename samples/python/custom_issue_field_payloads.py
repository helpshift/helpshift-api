"""

Notes:
    The payloads here assume that the following custom issue fields are present in the system.

        Name of field       Type of field
        
        1. item             dropdown
        2. gift_wrapped     checkbox
        3. order_id         singleline
        4. billing_name     singleline
        5. billing_address  multiline
        6. order_date       date
        7. quantity         number
        8. customer_id      number
        
"""

BASIC_PAYLOAD = {"email": "test@mail.com",
                 "message-body": "Custom Issue Fields Demo.",
                 "title": "Issue with random custom issue fields"}

PAYLOADS = [
    {"item": {"type": "dropdown",
              "value": "Cricket"},
     "gift_wrapped": {"type": "checkbox",
                      "value": "true"},
     "order_id": {"type": "singleline",
                  "value": "asdf1122"},
     "billing_name": {"type": "singleline",
                      "value": "Scott Broke"},
     "billing_address": {"type": "multiline",
                         "value": "King's Landing , London , UK"},
     "quantity": {"type": "number",
                  "value": 55},
     "order_date": {"type": "date",
                    "value": 1506988800000}},

    {"item": {"type": "dropdown",
              "value": "Chess"},
     "gift_wrapped": {"type": "checkbox",
                      "value": "true"},
     "order_id": {"type": "singleline",
                  "value": "asdf1234"},
     "billing_name": {"type": "singleline",
                      "value": "Scott Kane"},
     "billing_address": {"type": "multiline",
                         "value": "Eyrie, London , UK"},
     "quantity": {"type": "number",
                  "value": 60},
     "customer_id": {"type": "number",
                     "value": 10},
     "order_date": {"type": "date",
                    "value": 1507766400000}},

    {"item": {"type": "dropdown",
              "value": "Table Tennis"},
     "gift_wrapped": {"type": "checkbox",
                      "value": "false"},
     "order_id": {"type": "singleline",
                  "value": "asdf3456"},
     "billing_name": {"type": "singleline",
                      "value": "Scott Williams"},
     "billing_address": {"type": "multiline",
                         "value": "Old Town , Liverpool , UK"},
     "quantity": {"type": "number",
                  "value": 35},
     "customer_id": {"type": "number",
                     "value": 15},
     "order_date": {"type": "date",
                    "value": 1507248000000}},

    {"item": {"type": "dropdown",
              "value": "Basketball"},
     "gift_wrapped": {"type": "checkbox",
                      "value": "true"},
     "order_id": {"type": "singleline",
                  "value": "asdf5678"},
     "billing_name": {"type": "singleline",
                      "value": "scott tiger"},
     "billing_address": {"type": "multiline",
                         "value": "Assahai , Leeds , UK"},
     "quantity": {"type": "number",
                  "value": 70},
     "customer_id": {"type": "number",
                     "value": 13},
     "order_date": {"type": "date",
                    "value": 1507075200000}}]

FILTERS = [
    {"description": "Get all issues about orders with gift wrapped.",
     "query": {"checkbox": {"and": {"gift_wrapped": "true"}}}},

    {"description": "Get all issues about orders for Scott but not Broke or Williams.",
     "query": {"singleline": {"and": {"billing_name": {"is_set": "true",
                                                       "contains": ["Scott"],
                                                       "does_not_contain": ["Broke",
                                                                            "Williams"]}}}}},

    {"description": "Get all issues with orders for Scott but "
                    "not with order id 'asdf1234 or 'asdf5678'.",
     "query": {"singleline": {"and": {"billing_name": {"is_set": "true",
                                                       "contains": ["Scott"]},
                                      "order_id": {"is_set": "true",
                                                   "does_not_contain": ["asdf1234",
                                                                        "asdf5678"]}}}}},

    {"description": "Get all issues with address containing cities from UK but"
                    " not London or Liverpool.",
     "query": {"multiline": {"and": {"billing_address": {"is_set": "true",
                                                         "contains": ["UK"],
                                                         "does_not_contain": ["London",
                                                                              "Liverpool"]}}}}},

    {"description": "Get all issues with customers and with 50 <= quantity < 80 but not 60.",
     "query": {"number": {"and": {"customer_id": {"is_set": "true"},
                                  "quantity": {"is_set": "true",
                                               "is_not": 60,
                                               "is_smaller_than": 80}},
                          "or": {"quantity": {"is": 50,
                                              "is_greater_than": 50}}}}},

    {"description": "Get all issues for customer_id 15 but quantity below 40.",
     "query": {"number": {"and": {"customer_id": {"is": 15},
                                  "quantity": {"is_set": "true"}},
                          "or": {"quantity": {"is": 40,
                                              "is_smaller_than": 40}}}}},

    {"description": "Get all issues with item set to standard outdoor games.",
     "query": {"dropdown": {"and": {"item": {"is_set": "true",
                                             "is_not": "Table Tennis",
                                             "is_none_of": ["Chess",
                                                            "Carrom"]}},
                            "or": {"item": {"is": "Basketball",
                                            "is_one_of": ["Football",
                                                          "Cricket"]}}}}},

    {"description": "Get all issues with orders placed between 1st October and 10th October 2017,"
                    " but not on 6th October 2017.",
     "query": {"date": {"and": {"order_date": {"is_set": "true",
                                               "is_not": "1507248000000",
                                               "is_after": "1506729600000",
                                               "is_before": "1507680000000"}}}}},

    {"description": "Filtering on all field types.",
     "query": {"checkbox": {"and": {"gift_wrapped": "true"}},
               "singleline": {"and": {"billing_name": {"is_set": "true",
                                                       "contains": ["Kane"]},
                                      "order_id": {"is_set": "true"}}},
               "multiline": {"and": {"billing_address": {"is_set": "true",
                                                         "contains": ["London"]}}},
               "number": {"and": {"quantity": {"is_set": "true",
                                               "is_greater_than": 10},
                                  "customer_id": {"is_not": 15}}},
               "dropdown": {"and": {"item": {"is_set": "true",
                                             "is_not": "Football"}}},
               "date": {"and": {"order_date": {"is_set": "true",
                                               "is_after": "1507593600000"}}}}}]
