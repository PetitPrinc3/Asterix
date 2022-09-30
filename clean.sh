#!/bin/bash

docker container kill frontend
docker container kill backend

for i in $(docker ps -a | cut -d " " -f 1 | grep -v CONTAINER):
do
    docker container kill $i
    docker container rm $i --force
done

for i in $(docker ps -a | cut -d " " -f 4):
do
    docker image rm $i --force
done

docker image rm frontend --force
docker image rm backend --force

docker volume rm InputFiles --force
docker volume rm OutputFiles --force
docker volume rm SharedDB --force

rm -r /src
rm /opt/docker_runner/boot.sh
rm /opt/docker_runner/run.sh

cd ..
rm -r Asterix