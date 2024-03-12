Writeup: Solución al challenge basic-mod1- picoctf

Este reto CTF de criptografía pertenece a la página de picoCTF: https://play.picoctf.org/practice/challenge/253?category=2&page=2
Básicamente nos dan un .txt con números en donde debemos descifrar el mensaje para ingresar la flag.

![image](https://github.com/frangodoy00/CTFS-Writeups/assets/62100382/34d79172-373e-4284-a1c6-39bba375853d)


![image](https://github.com/frangodoy00/CTFS-Writeups/assets/62100382/e4cbca01-28e0-4fb6-b03f-a6dc4f522e1b)

Lo que dice es que a partir del mensaje .txt a cada número realizarle un mod 37. Para luego convertir si está entre 0 y 25 a la letra correspondiente del alfabeto en formato uppercase. Si se encuentra entre 26 y 35 convertir a dígito decimal y si fuese el número 37, convertir a “_”.

Solución:
Para resolver dicho reto realicé un script en python para que fuese más sencillo calcular los mod y realizar las conversiones de los caracteres. Dicho script se encuentra en la misma carpeta.


![image](https://github.com/frangodoy00/CTFS-Writeups/assets/62100382/07cf1d8c-82ee-4316-b1d1-9d05afbe4b36)

Lo que hace el anterior script es primero leer números del .txt y guardarlos en una lista temporal en formato int.
Luego a cada elemento de la lista, es decir, a cada número realizarle la operación mod 37 como dice el enunciado para después chequear si se encuentra entre 0 y 25, entre 26 y 35, ó es 36.
Una vez que tome un camino u otro se agrega a la lista “flag” convirtiendo previamente con la librería string en el formato que tenga que realizarse la conversión.
Finalmente imprimimos la flag con los resultados luego de haber realizado las conversiones.

Flag:
picoCTF{R0UND_N_R0UND_ADD17EC2}
