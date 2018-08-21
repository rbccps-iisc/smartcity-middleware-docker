#!/usr/bin/env bash
curl -ik -X POST "https://localhost:8443/api/1.0.0/publish/$1.protected" -H "apikey: $2" -d '{"body": "testdata"}'
