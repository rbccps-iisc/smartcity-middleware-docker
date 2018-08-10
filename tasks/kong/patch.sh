#!/bin/ash

RED='\033[0;31m'
NC='\033[0m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'

echo -e "${YELLOW}[  INFO  ]${NC} Deleting API upstream URL"

curl -XDELETE "http://localhost:8001/apis/register"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Success Deleting API upstream URL"
else
    echo -e "${RED}[ ERROR ]${NC} Failure Deleting API upstream URL"
fi

echo -e "${YELLOW}[  INFO  ]${NC} Updating PATCH"

curl -XPOST "http://localhost:8001/apis/" -d 'name=register&upstream_url=http://webserver:8080/cdx/register&uris=/api/1.0.0/register&methods=POST'

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Success Creating API upstream URL"
else
    echo -e "${RED}[ ERROR ]${NC} Failure Creating API upstream URL"
fi

echo -e "${YELLOW}[  INFO  ]${NC} Updating PATCH"

curl -XPOST "http://localhost:8001/apis/register/plugins" -d 'name=key-auth'

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Success Creating API upstream URL Key-Auth"
else
    echo -e "${RED}[ ERROR ]${NC} Failure Creating API upstream URL Key-Auth"
fi

echo -e "${YELLOW}[  INFO  ]${NC} Updating PATCH"

curl -XPOST "http://localhost:8001/apis/register/plugins" -d 'name=acl&config.whitelist=provider'

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Success Creating API upstream URL Key-Auth ACL"
else
    echo -e "${RED}[ ERROR ]${NC} Failure Creating API upstream URL Key-Auth ACL"
fi
