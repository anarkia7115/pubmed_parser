curl --header "Content-Type: application/json" \
     --request POST \
          --data '{"ak":"PCRMSH5O7SEJIKFA70P1", "sk":"5ajzWsnQ7t12lQ2qcx17SxSmwHE9Xg0XHHaK8fWr", "path": "pubmed_baseline/pubmed19n0971.xml.gz", "limit": 1 }' \
               http://localhost:5000/parse_pubmed

