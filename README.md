# Parse Pubmed
## Improvements
* Dockerized
* Kafka Input/Output

## How to run
`envsubst < ./kubernetes/pubmed-parser-deploy.yaml | kubectl apply -f -`

## Running command for python module
` ["python3", "-m", "server.kafka_consumer", "kafka:9092", "gzfiles", "pubmeds"] `

## Kafka input
Input topic: gzfiles
Input format: { "path": "pubmed_baseline/pubmed19n0971.xml.gz", "limit": 10 }

## Kafka output
Output topic: pubmeds
Output format: JsonLines


