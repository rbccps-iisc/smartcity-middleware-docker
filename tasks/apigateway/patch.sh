#!/bin/ash

RED='\033[0;31m'
NC='\033[0m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'

echo -e "${YELLOW}[  INFO  ]${NC} Deleting API upstream URL"

curl -XDELETE "http://localhost:8001/apis/landing"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Success Deleting Landing API upstream URL"
else
    echo -e "${RED}[ ERROR ]${NC} Failure Deleting Landing API upstream URL"
fi

echo -e "${YELLOW}[  INFO  ]${NC} Updating PATCH"

curl -XPOST "http://localhost:8001/apis/" -d 'name=landing&upstream_url=http://webserver:8080/cdx/redirect&uris=/&methods=GET'

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Success Creating Landing API upstream URL"
else
    echo -e "${RED}[ ERROR ]${NC} Failure Creating Landing API upstream URL"
fi

echo -e "${YELLOW}[  INFO  ]${NC} Deleting Register API upstream URL"

curl -XDELETE "http://localhost:8001/apis/register"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Success Deleting Register API upstream URL"
else
    echo -e "${RED}[ ERROR ]${NC} Failure Deleting Register API upstream URL"
fi

echo -e "${YELLOW}[  INFO  ]${NC} Updating PATCH"

curl -XPOST "http://localhost:8001/apis/" -d 'name=register&upstream_url=http://webserver:8080/cdx/register&uris=/api/1.0.0/register&methods=POST'

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Success Creating Register API upstream URL"
else
    echo -e "${RED}[ ERROR ]${NC} Failure Creating Register API upstream URL"
fi

echo -e "${YELLOW}[  INFO  ]${NC} Updating PATCH"

curl -XPOST "http://localhost:8001/apis/register/plugins" -d 'name=key-auth'

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Success Creating Key-Auth"
else
    echo -e "${RED}[ ERROR ]${NC} Failure Creating Key-Auth"
fi

echo -e "${YELLOW}[  INFO  ]${NC} Updating PATCH"

curl -XPOST "http://localhost:8001/apis/register/plugins" -d 'name=acl&config.whitelist=provider'

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[   OK   ]${NC} Success Creating ACL"
else
    echo -e "${RED}[ ERROR ]${NC} Failure Creating ACL"
fi
