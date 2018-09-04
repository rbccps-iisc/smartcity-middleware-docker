#!/usr/bin/env ash
curl -k -X POST \
  "https://localhost:8443/api/1.0.0/register" \
  -H 'apikey: '$1'' \
  -H 'content-type: application/json' \
  -d '{
   "id": '$2'
}' 2>/usr/local/apigateway/database_error.log >/usr/local/apigateway/database_out.log
