# Writeup: Solución al challenge TJCTF 2023 | web/swill-squill

Se presenta el reto

<img width="835" alt="Screenshot 2023-05-27 at 19 09 15" src="https://github.com/JCAlmazan/CTFS-Writeups/assets/25467138/48124dc5-787b-4573-9dd3-64f5ecf632a8">

Descargamos el .zip y lo abrimos en un editor de texto. 

Abrimos la web y nos encontramos con los dos campos.

<img width="1792" alt="Screenshot 2023-05-27 at 18 58 34" src="https://github.com/JCAlmazan/CTFS-Writeups/assets/25467138/ff2c3b71-1fa2-4c7b-95c2-b288e6145f6a">

Analizamos la request cuando rellenamos el formulario.

<img width="1792" alt="Screenshot 2023-05-27 at 19 13 55" src="https://github.com/JCAlmazan/CTFS-Writeups/assets/25467138/9acd13f4-2fa0-401d-85fe-a69f37a5c9c6">

Agregamos una nota y vemos que se lista.

<img width="1792" alt="Screenshot 2023-05-27 at 19 15 55" src="https://github.com/JCAlmazan/CTFS-Writeups/assets/25467138/46db2386-a24d-4975-81ac-9dbe63139a00">

Ahora miramos el código provisto.
<img width="742" alt="Screenshot 2023-05-27 at 19 16 27" src="https://github.com/JCAlmazan/CTFS-Writeups/assets/25467138/41a9961c-7ec3-4f39-9724-7bae7494a46b">
Vemos que nos muestra las notas que son nuestras.

El flag se encuentra en la tabla notes, para el dueño "admin"

<img width="549" alt="Screenshot 2023-05-27 at 19 16 50" src="https://github.com/JCAlmazan/CTFS-Writeups/assets/25467138/3f769188-9da7-4e08-acad-d62cc2923bc2">

Intentamos loguearnos como admin, pero nos redirecciona y no nos deja loguearnos.

<img width="467" alt="Screenshot 2023-05-27 at 19 17 22" src="https://github.com/JCAlmazan/CTFS-Writeups/assets/25467138/37474469-8f5a-4483-b14f-d1fd731f8ee8">

## Solución:

Usamos sql injection para obtener las notas de "admin" sin que nuestro usuario sea "admin".

Para ello nos creamos un usuario con el siguiente nombre: admin'; --
De esta forma, cuando obtengamos las notas, obtendremos las de admin, ya que con los dos guiones creamos un comentario en la consulta para lo que viene después.

<img width="1792" alt="Screenshot 2023-05-27 at 19 20 20" src="https://github.com/JCAlmazan/CTFS-Writeups/assets/25467138/c288b588-e45a-4a7b-a930-e8f443cd9870">

Finalmente, se listan las notas de admin, incluyendo el flag.

<img width="1792" alt="Screenshot 2023-05-27 at 19 20 29" src="https://github.com/JCAlmazan/CTFS-Writeups/assets/25467138/0945f5d8-3f1d-4f52-b4d2-a0a24210ffe1">



## Flag

Ingresamos el flag y es correcto.

<img width="838" alt="Screenshot 2023-05-27 at 19 20 50" src="https://github.com/JCAlmazan/CTFS-Writeups/assets/25467138/4103df36-a39e-4bdc-9285-0742ed602f2a">


<img width="344" alt="Screenshot 2023-05-27 at 19 20 55" src="https://github.com/JCAlmazan/CTFS-Writeups/assets/25467138/891419a0-ea37-4042-815c-a6ee55baa142">


`tjctf{swill_sql_1y1029345029374}`

*Enlace: [https://ctftime.org/event/1865](https://ctftime.org/event/1865)*
