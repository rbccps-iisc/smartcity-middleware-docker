#!/usr/bin/env bash
curl -ik -X POST https://localhost:8443/api/1.0.0/share \
-H "apikey: $1" \
-d '{"entityID": '"$2"', "permission":"read"}'
