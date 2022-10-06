#!/bin/bash

docker container rm frontend --force
docker container rm backend --force
docker container rm brain --force


docker image rm frontend --force
docker image rm backend --force
docker image rm brain --force


docker volume prune


docker ps -a
docker container ls
docker images
docker volume ls


cd ..
rm -r Asterix

git clone https://github.com/G4vr0ch3/Asterix
