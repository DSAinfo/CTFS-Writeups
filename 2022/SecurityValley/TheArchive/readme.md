# Writeup: Solución al challenge SecurityValley - The Archive

Este es un reto de CTF en el que tenemos que encontrar la contraseña de un archivo .zip protegido para poder descomprimirlo y acceder a su contenido.

<img width="471" alt="imagen1" src="https://user-images.githubusercontent.com/37942177/221001358-50aac079-627d-4b6b-8594-b359eadd3c0a.png">

## Paso 1: Inspección inicial
Accedemos al repositorio y descargamos el archivo "archive.zip".
Al intentar descomprimirlo, nos dimos cuenta de que estaba protegido con contraseña y no la conocíamos.

<img width="408" alt="imagen2" src="https://user-images.githubusercontent.com/37942177/221001445-565b493a-b274-4cb0-a249-087dd4674ce8.png">

## Paso 2: Eleccion de una herramienta de fuerza bruta
Decidimos utilizar una herramienta de fuerza bruta para intentar descifrar la contraseña. Elegimos utilizar la herramienta fcrackzip porque está especialmente diseñado para descifrar contraseñas en archivos .zip y es conocido por su eficacia en este tipo de ataques.Tambien habiamos considerado otras herramientas como John the Ripper o Hashcat.

En cuanto a la elección del diccionario, optamos por utilizar el archivo "rockyou.txt" debido a que es uno de los diccionarios de contraseñas más populares y completos disponibles en la actualidad. Este archivo contiene millones de contraseñas comunes y frecuentemente utilizadas, lo que aumenta las posibilidades de que se encuentre la contraseña del archivo .zip protegido.

## Paso 3: Ejecución del comando de fuerza bruta
Ejecutamos el siguiente comando en la terminal: 

```bash
fcrackzip -v -D -u -p rockyou.txt archive.zip
```
"-v": modo verboso, es decir, muestra información adicional durante la ejecución.

"-D": indica que se va a utilizar un diccionario para el ataque de fuerza bruta.

"-u": permite descomprimir el archivo a medida que se intenta descifrar la contraseña.

"-p rockyou.txt": especifica el diccionario de contraseñas a utilizar. En este caso, se está utilizando el archivo de texto "rockyou.txt".

"archive.zip": el nombre del archivo ZIP cifrado que se va a atacar.

## Paso 4: Encontramos la contraseña
Esperamos a que el proceso de fuerza bruta finalizara y efectivamente encontramos la contraseña.

<img width="610" alt="imagen3" src="https://user-images.githubusercontent.com/37942177/221001593-fc7c3e70-69bb-4fe7-8e74-0e39a61d3d27.png">



## Paso 5: Descomprimir y resolver el reto
Una vez obtenida la contraseña, intentamos descomprimir el archivo con la contraseña encontrada, lo que nos permitió acceder al contenido del archivo y resolver el reto.

<img width="94" alt="Captura de pantalla 2023-02-20 a la(s) 15 44 37" src="https://user-images.githubusercontent.com/37942177/221001668-9820e6e5-2469-4597-8d15-f04e708f0c6f.png"> <img width="692" alt="imagen4" src="https://user-images.githubusercontent.com/37942177/221002024-57b3ab61-7ea1-426b-9820-fd87d818ba3c.png">
<img width="806" alt="imagen5" src="https://user-images.githubusercontent.com/37942177/221002369-9fe6cd32-a8d6-4438-bb8f-df52461750d7.png">
<img width="809" alt="imagen6" src="https://user-images.githubusercontent.com/37942177/221002392-7a32e36d-397e-49f8-b487-618f0421408c.png">



## Conclusion
En resumen, la solución al challenge SecurityValley - The Archive involucró la elección de una herramienta de fuerza bruta (fcrackzip) y un diccionario de contraseñas popular (rockyou.txt) para descifrar la contraseña de un archivo .zip protegido y acceder a su contenido.
