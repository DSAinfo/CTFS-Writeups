# Tipo: Miscellaneous Desafío: Out of the bucket 1

![image](https://github.com/LauAria/CTFS-Writeups/assets/48163730/e149e0bc-e3bc-4fc1-9f5e-9797d414b08b)

El desafio nos da este link https://storage.googleapis.com/out-of-the-bucket/src/index.html el cual nos lleva a una página donde se ven dos imágenes de banderas.

![image](https://github.com/LauAria/CTFS-Writeups/assets/48163730/fc8e221f-a2cc-4ea9-83db-cc45cf55caab)

Para resolverlo lo primero que miramos fueron las imágenes, al no encontrar ninguna información escondida dentro, vimos donde estaban guardadas, lo cual era un storge de google: https://storage.googleapis.com/out-of-the-bucket/
dicho storage al entrar sin el path a la imagen (/src/index.html) te lleva a la raíz donde se ve todo el contenido de este storage en XML

![image](https://github.com/LauAria/CTFS-Writeups/assets/48163730/63554198-aba6-4c16-91a0-0991bc53e391)

particularmente en la ruta secret/dont_show se descarga un archivo el cual contiene la flag: 

uoftctf{allUsers_is_not_safe}

