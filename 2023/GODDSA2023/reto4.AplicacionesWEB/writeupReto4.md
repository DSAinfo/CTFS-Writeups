Writeup: Solución al challenge Local Authority picoctf

Este reto CTF de Explotación WEB pertenece a la página de picoCTF:
https://play.picoctf.org/practice/challenge/278?category=1&page=2

Lo que propone el reto es poder encontrar la flag oculta en la aplicacíón web proporcionada, a través de un login: http://saturn.picoctf.net:59126/

![image](https://github.com/frangodoy00/CTFS-Writeups/assets/62100382/0970c4db-daae-40ee-8cb0-8d2a08ea1f69)

Solución:

Para resolver este reto es de gran ayuda la consola web que proporciona el navegador para inspeccionar el código de la página y otras funcionalidades.
Al realizar un intento de inicio de sesion con cualquier usuario y contraseña podemos ver que se realiza un "disparo" y podemos visualizar una serie de archivos que antes no podiamos ver:

![image](https://github.com/frangodoy00/CTFS-Writeups/assets/62100382/08ae8611-5ae4-4912-ae8c-8c47197b08bc)

Si inspeccionamos el archivo secure.js podemos ver que en el if() se muestran explicitamente las credenciales para pasar el login:

![image](https://github.com/frangodoy00/CTFS-Writeups/assets/62100382/86402927-fc8c-4b36-89ba-32d707acb300)

Una vez logeados se nos muestra finalmente la flag en pantalla para finalizar con este reto.

Flag:
picoCTF{j5_15_7r4n5p4r3n7_a8788e61}
