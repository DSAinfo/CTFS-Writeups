#!/bin/bash

# Volver a empezar. Ideal para cuando se perdieron en los cambios que estaban haciendo.

docker-compose down
docker-compose up -d --build
docker-compose cp bwapp:/var/www/html/insecure_direct_object_ref_1.php ./insecure_direct_object_ref_1.php
docker-compose cp bwapp:/var/www/html/insecure_direct_object_ref_2.php ./insecure_direct_object_ref_2.php
