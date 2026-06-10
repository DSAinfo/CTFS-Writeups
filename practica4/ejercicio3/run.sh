#!/bin/bash

docker build -t practica2 .
docker build -t pythonbase .

docker-compose up
