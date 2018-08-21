#!/usr/bin/env bash
curl -k -X GET "https://localhost:8443/api/1.0.0/subscribe/$1/1" -H "apikey: $2"
