#!/usr/bin/env bash
curl -ik -X DELETE https://localhost/api/1.0.0/register -H 'apikey: guest' -d '{"entityID": "apitestingdashboard"}'
