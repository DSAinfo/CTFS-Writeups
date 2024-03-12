Writeup: Solución al challenge Includes picoctf

Este reto CTF de Explotación WEB pertenece a la página de picoCTF:
https://play.picoctf.org/practice/challenge/274?category=1&page=2
Lo que propone el reto es poder encontrar la flag oculta en la aplicacíón web proporcionada: http://saturn.picoctf.net:50761/

![image](https://github.com/frangodoy00/CTFS-Writeups/assets/62100382/c059df7d-9f5e-467a-8336-ef4106771af5)

Solución:

Para resolver este reto es de gran ayuda la consola web que proporciona el navegador para inspeccionar el código de la página y otras funcionalidades.


![image](https://github.com/frangodoy00/CTFS-Writeups/assets/62100382/09ee53c0-826e-4e2f-a5d4-eb2ad13b46ce)

Podemos notar que la página se compone de 3 archivos. Un index.html, un script.js y un style.css.
Vemos que el botón que contiene la página ejecuta el script.js y si lo inspeccionamos:

![image](https://github.com/frangodoy00/CTFS-Writeups/assets/62100382/32775fa8-741e-41a7-b129-2d204b96fb47)

Notamos que se encuentra comentado el final de la flag. Por lo tanto debemos encontrar la primera parte. E inspeccionando el archivo style.css:

![image](https://github.com/frangodoy00/CTFS-Writeups/assets/62100382/a522c02f-b3f3-4799-8c54-26ad5f8af4ff)

Podemos ver que se encuentra comentada la primera parte de la flag. Finalmente si unimos ambas podemos determinar cual es la flag para ingresarla en el reto.

Flag:
picoCTF{1nclu51v17y_1of2_f7w_2of2_df589022}
