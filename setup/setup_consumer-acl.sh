#!/usr/bin/env ash
curl -X POST "http://kong:8001/consumers/$1/acls" \
    --data "group=provider"