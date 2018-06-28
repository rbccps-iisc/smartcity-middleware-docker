#!/usr/bin/env bash
curl -ik -X GET "http://localhost:11000/api/1.0.0/subscribe?name=streetlight"
-H "apikey: $1"
