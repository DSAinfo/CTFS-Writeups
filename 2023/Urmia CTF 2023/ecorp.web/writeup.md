![img_1](https://github.com/emilianosecchi/CTFS-Writeups/assets/49136614/b789598d-9865-4c6a-83ab-62c45336f692)

En un principio recuperamos la ip del dominio ecorpblog.uctf.ir, para poder acceder a ella e ir probando distintas urls para ver si conseguíamos acceder al panel. Esto no resultó, por lo que volvimos al blog y empezamos a analizar si encontrábamos algo oculto en él. 
Luego de ver la pestaña de network del navegador, observamos que se llamaba a una api que devolvía los posteos que habían hecho los usuarios.

![img_2](https://github.com/emilianosecchi/CTFS-Writeups/assets/49136614/cc70cc3d-d972-42a8-8c55-e6b04d2d970a)

En el request se puede ver que está pasándose el nombre de un archivo. Con esto se nos ocurrió abrir postman y empezar a probar directorios que creíamos que podían contener información. El primero que probamos fue el de la propia api, para ver qué hacía el código por atrás:

![img_3](https://github.com/emilianosecchi/CTFS-Writeups/assets/49136614/9d4d89cc-2bf4-47a9-a050-4e5c328f0577)

Acá vimos que hace un file_get_contents para recuperar el archivo que le pasamos por parámetro, por lo que seguimos probando con otros archivos como /etc/apache2/sites-enabled/000-default.conf o los logs de /var/log/access.log, pero no teníamos éxito. 
Luego de un rato nos pusimos a analizar por qué indicaba file:// antes del archivo, y pensamos que quizás se podían recuperar archivos por otro protocolo como http://. El resultado fue el siguiente:

![img_4](https://github.com/emilianosecchi/CTFS-Writeups/assets/49136614/d605f6b5-a574-4e19-b787-6e52ff09619a)
