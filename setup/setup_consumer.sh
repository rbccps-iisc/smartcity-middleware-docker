#!/usr/bin/env ash
curl -i -k -X POST \
  "http://kong:8001/consumers/" \
  --data "username=$1"