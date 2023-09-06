![img_1](https://github.com/emilianosecchi/CTFS-Writeups/assets/49136614/e3a2e427-5437-4b8a-bcfa-9bc486321372)

Para este reto, descargamos la captura de paquetes y un archivo con las master keys para TLS. Como primera medida, editamos las preferencias de Wireshark para el protocolo TLS y agregamos el archivo descargado en el master-secret log.

![img_2](https://github.com/emilianosecchi/CTFS-Writeups/assets/49136614/f5a558f5-bd82-4d51-a5c0-d8b54b59c3a9)

Posterior a esto, filtramos en Wireshark todos los paquetes que fueron enviados utilizando el protocolo TLS, indicando el server name ‘mrgray’, el cual se nombraba en el enunciado del CTF.

![img_3](https://github.com/emilianosecchi/CTFS-Writeups/assets/49136614/52c397c0-ac80-4824-8fcd-72fa0ab54e49)

Siguiendo el stream TLS del primer paquete filtrado, se puede ver toda la comunicación HTTP encriptada, en la cual se encontraba oculto el flag del reto.

![img_4](https://github.com/emilianosecchi/CTFS-Writeups/assets/49136614/796e06c5-995b-462b-bcfb-20f47ee25f51)
