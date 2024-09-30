El URL incluido en el CTF lleva a una aplicación web muy simple que tiene un login y un botón para obtener la flag.

El botón de la flag no funciona sin sesión, luego de crearnos un usuario en la aplicación nos logueamos (en nuestro caso usamos un usuario *cu3nt4r4nd0mm*), e intentamos presionar el botón, pero cuando cargó la pantalla aparecía *unauthorized*.

Luego de un par de intentos tomamos el token JWT que se genera al iniciar sesión, y lo pasamos por un decoder de JWT. La parte del payload contenía la siguiente información:

```
{
  "name": "cu3nt4r4nd0mm",
  "admin": false
}
```

Al modificar el payload, reemplazando el false por *true*, se modificó el token y actualizamos el header HTTP con el nuevo token generado. Cuando recargamos la página que muestra el flag pudimos verla:

FLAG: **LITCTF{o0ps_forg0r_To_v3rify_1re4DV9}**