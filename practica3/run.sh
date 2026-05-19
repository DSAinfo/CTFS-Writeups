#!/bin/bash

docker build -t practica3 .

if command -v docker-compose &> /dev/null; then
  echo "docker-compose is installed (legacy version)."
	docker-compose up
else
	docker compose up
fi