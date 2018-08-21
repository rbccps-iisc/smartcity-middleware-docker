#!/bin/bash
curl -ikX POST \
  https://localhost:8443/api/1.0.0/follow \
  -H 'Content-Type: application/json' \
  -H 'apikey: '$1'' \
  -d '{"entityID": "'$2'", "permission":"read", "validity": "10D"}'
