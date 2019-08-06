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

## Kafka output
Output topic: pubmeds


