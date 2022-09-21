#!/bin/bash

docker container kill frontend --force
docker container kill Backend --force

docker container rm frontend --force
docker container rm Backend --force

docker image rm frontend --force
docker image rm Backend --force

docker volume rm InputFiles --force
docker volume rm OutputFiles --force
docker volume rm SharedDB --force

rm -r /src
rm /opt/docker_runner/boot.sh
rm /opt/docker_runner/run.sh

cd ..
rm -r IMOTEP