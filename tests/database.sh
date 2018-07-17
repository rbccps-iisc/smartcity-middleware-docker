#!/usr/bin/env bash
curl --insecure -i -X GET http://localhost:11000/api/1.0.0/db?pretty=true\&sort=@timestamp:desc\&size=1 \
-H 'content-type: application/json' \
-H "apikey: $1" \
-d '{ "query": { "match": { "routing-key": "streetlight" } } }'
