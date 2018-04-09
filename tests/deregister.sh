#!/usr/bin/env bash
curl -ik -X DELETE https://localhost:10443/api/1.0.0/register -H 'apikey:  guest' -d '{"entityID": "dashboard"}'