#!/usr/bin/env bash
curl -ik -X POST "http://localhost/api/1.0.0/publish" -H "apikey: $1" -d '{"body": "travis test"}'
