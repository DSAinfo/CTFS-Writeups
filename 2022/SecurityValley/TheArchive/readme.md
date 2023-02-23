
# Writeup: Solución al challenge SecurityValley - The Archive

Este es un reto de CTF en el que tenemos que encontrar la contraseña de un archivo .zip protegido para poder descomprimirlo y acceder a su contenido.

## Paso 1: Inspección inicial
Accedemos al repositorio y descargamos el archivo "archive.zip".
Al intentar descomprimirlo, nos dimos cuenta de que estaba protegido con contraseña y no la conocíamos.


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
Esperamos a que el proceso de fuerza bruta finalizara y efectivamente encontramos la contraseña

## Paso 5: Descomprimir y resolver el reto
Una vez obtenida la contraseña, intentamos descomprimir el archivo con la contraseña encontrada, lo que nos permitió acceder al contenido del archivo y resolver el reto.

## Conclusion
En resumen, la solución al challenge SecurityValley - The Archive involucró la elección de una herramienta de fuerza bruta (fcrackzip) y un diccionario de contraseñas popular (rockyou.txt) para descifrar la contraseña de un archivo .zip protegido y acceder a su contenido.