#!/bin/bash 
i=0
while [ $i -lt 1000 ]; 
do
curl -i -k -X POST "http://localhost:32768/api/0.1.0/publish" -H 'apikey: 79a7c7ed9aef4b848abf71e75f358fbb' -d '{"exchange": "amq.topic", "key": "testDemo", "body": "Command Data"}'
let i=i+1
done
