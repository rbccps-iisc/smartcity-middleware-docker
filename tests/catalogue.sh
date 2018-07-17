#!/usr/bin/env bash
curl -k -X GET http://localhost:11000/api/1.0.0/cat?id=$1
