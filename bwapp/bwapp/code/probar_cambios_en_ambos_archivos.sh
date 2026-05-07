#!/bin/bash

# Escribir ambos archivos .php en el contenedor

docker-compose cp ./insecure_direct_object_ref_1.php bwapp:/var/www/html/insecure_direct_object_ref_1.php
docker-compose cp ./insecure_direct_object_ref_2.php bwapp:/var/www/html/insecure_direct_object_ref_2.php
