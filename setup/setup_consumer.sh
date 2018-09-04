#!/usr/bin/env ash
curl -i -k -X POST \
  "http://apigateway:8001/consumers/" \
  --data "username=$1"