#!/usr/bin/env bash
curl -ik -X POST https://localhost:10443/api/1.0.0/publish -H "apikey: $1" -d '{"body": "travis test"}'