#!/usr/bin/env bash
curl -ik -X GET "https://localhost/api/1.0.0/subscribe?name=streetlight"
-H "apikey: $1"
