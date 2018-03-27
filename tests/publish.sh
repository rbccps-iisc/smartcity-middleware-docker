#!/usr/bin/env bash
i="0"
while [ $i -lt 10000000 ]
do
curl -ik -X POST https://localhost:10443/api/1.0.0/publish -H "apikey: $1" -d '{"body": "travis test"}'
i=$[$i+1]
done