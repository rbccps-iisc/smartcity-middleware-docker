#!/usr/bin/env bash
curl -ik -X POST "https://localhost:8443/api/1.0.0/publish/apitestingstreetlight.protected" -H "apikey: $1" -d '{"body": "travis test"}'
