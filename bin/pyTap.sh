#!/usr/bin/env bash
set -v
# Stop
docker stop pythontap

# Remove previuos container 
docker container rm pythontap

docker build ../python/ --tag tap:python

PYTHON_APP=$1
shift
# Running python app
docker run -e PYTHON_APP=$PYTHON_APP  --network tap --name pythontap -it tap:python $@