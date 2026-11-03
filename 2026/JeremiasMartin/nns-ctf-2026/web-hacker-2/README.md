## NNS CTF 2026

# Web Hacker 2

**CTF:** NNS CTF 2026  
**Categoría:** Web  
**Dificultad:** Beginner  
**Autor:** pipreth  
**Fecha de resolución:** 06/09/2026  
**Reto:** [Web Hacker 2](https://nnsc.tf/)  
**Evento:** [NNS CTF 2026 - CTFtime](https://ctftime.org/event/3097)

![Portada del evento](./imágenes/Imagen%20pegada.png)

![Portada del reto Web Hacker 2](./imágenes/Imagen%20pegada%20(2).png)


Al iniciar la instancia del reto accedemos al endpoint `/boarding-pass`.


La aplicación muestra una tarjeta de embarque correspondiente al vuelo **NNS 4043**, con una determinada ruta.

![Tarjeta de embarque mostrada por la aplicación](./imágenes/Imagen%20pegada%20(3).png)

Entre la información del vuelo podemos ver:

```text
Pasajero: DOE/JOHN
Identificación del vuelo: NNS 4043
Ruta: ENGM → ENZV
Puerta: A8
Asiento: 17E
```

La tarjeta también posee un código QR que al escanearlo obtenemos el siguiente mensaje:

```text
no flag here. What happens behind the scenes?
```

Este mensaje nos indica que la flag no se encuentra directamente dentro del QR y que debemos chequear qué ocurre internamente cuando se carga la tarjeta de embarque.

Para poder entender cómo obtiene la aplicación los datos mostrados en pantalla, inspeccionamos el código HTML mediante las herramientas de desarrollador del navegador (`F12`).

Dentro del código nos encontramos el script encargado de solicitar la información correspondiente a la tarjeta de embarque.

![Script encargado de obtener los datos de la tarjeta de embarque](./imágenes/Imagen%20pegada%20(4).png)

En el código podemos observar la estructura:

```javascript
// You are signed in as john.
const username = 'john';

fetch('/api/boarding-pass/' + username)
  .then((a) => {
    a.json().then((b) => {
      // ...
    });
  });
```

La primera información que nos resulta útil es el comentario:

```javascript
// You are signed in as john.
```

que se setea en:

```javascript
const username = 'john';
```

Es decir, la app considera a `john` como usuario que está actualmente autenticado.
Posteriormente, ese nombre de usuario se concatena directamente con el endpoint `/api/boarding-pass/`, generando un requerimiento de esta forma:

```text
/api/boarding-pass/john
```

La respuesta que se obtiene desde este endpoint se va a usar luego por JavaScript para completar los distintos campos de la tarjeta de embarque.


Como podemos ver en la estructura propia del endpoint, el identificador del user forma parte de la URL.

```text
/api/boarding-pass/{username}
```

Esto nos va a permitir comprobar si el servidor realmente chequea que el usuario solicitado coincide con el usuario autenticado o si confía únicamente en el identificador pasado como parámetro en la URL.

Como primera referencia sabemos que la aplicación usa `/api/boarding-pass/john` para obtener la información propia del usuario `john`.

Teniendo en cuenta toda esta información procedemos a modificar manualmente el identificador por otro usuario relevante, como lo es el administrador:

```text
/api/boarding-pass/admin
```

De esta forma solicitamos directamente al servidor la tarjeta de embarque correspondiente al usuario `admin` sin modificar nuestra sesión ni autenticarnos con este rol.

Al realizar el requerimiento al endpoint correspondiente a `admin`, el servidor responde correctamente y devuelve un JSON con la información de su tarjeta de embarque.

![Respuesta JSON correspondiente al usuario admin](./imágenes/Imagen%20pegada%20(5).png)

Entre los datos devueltos encontramos:

```text
...
username: "admin"
route: 1337
fromName: "Stavanger"
fromCode: "ENZV"
toCode: "FLAG"
gate: "B2"
boarding: "12:00"
departure: "12:20"
passenger: "FLAG/ADMIN"
group: "0"
seat: "1A"
...
```

El campo más importante de la respuesta es `toName` que contiene el valor de la flag:
```text
NNS{yoU_4re_Now_1337_h4cKeR_1nd3eD}
```

A modo de resumen, al modificar el identificador utilizado por el endpoint pudimos acceder a información correspondiente a otro usuario y obtener directamente la flag del reto.  
Esta vulnerabilidad, vista en la materia, se conoce como **IDOR (Insecure Direct Object Reference)**.

Finalmente, ingresamos la flag obtenida en la plataforma del CTF, quedando el reto resuelto de forma correcta.

![Ingreso de la flag obtenida en Web Hacker 2](./imágenes/Imagen%20pegada%20(6).png)

![Challenge solved del reto Web Hacker 2](./imágenes/Imagen%20pegada%20(7).png)