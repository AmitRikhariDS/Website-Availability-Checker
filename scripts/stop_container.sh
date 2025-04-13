#!/bin/bash
set -e

container_id=docker ps | awk -f "" '{print $1}'
docker rm -f container_id