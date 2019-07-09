#!/bin/bash
envsubst < ./pubmed-parser-deploy.yaml | kubectl apply -f -
