#!/usr/bin/env bash
curl -ik -X DELETE http://localhost:11000/api/1.0.0/register -H 'apikey: guest' -d '{"entityID": "apitestingdashboard"}'
