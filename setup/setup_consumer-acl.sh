#!/usr/bin/env ash
curl -X POST "http://apigateway:8001/consumers/$1/acls" \
    --data "group=provider"