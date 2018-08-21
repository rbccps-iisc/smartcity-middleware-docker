#!/bin/bash
curl -ik -X GET \
  https://localhost:8443/api/1.0.0/bind/$1/$2 \
  -H 'apikey: '$3'' \
  -H 'routingKey: #'
