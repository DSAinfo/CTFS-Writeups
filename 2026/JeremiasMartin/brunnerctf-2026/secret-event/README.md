# Evento secreto

**CTF:** BrunnerCTF 2026  
**Categoría:** Web  
**Dificultad:** Fácil  
**Autor:** HLVM  
**Fecha de resolución:** 21/08/2026  
**Reto:** [Evento secreto](https://global.brunnerctf.dk/challenges#Secret%20Event-13)


![Portada](./imágenes/Pasted%20image%2020260822010409.png)

![Información del reto](./imágenes/Pasted%20image%2020260821230058.png)

El reto presenta una app web de **Brunnerne Inc.** destinada a la gestión de eventos corporativos. Al ingresar encontramos una página bastante simple, con las opciones de crear una cuenta o iniciar sesión.

![Página principal](./imágenes/Pasted%20image%2020260821222329.png)

![Login](./imágenes/Pasted%20image%2020260821222337.png)

![Registro](./imágenes/Pasted%20image%2020260821222351.png)

Como primer paso creamos una cuenta de prueba con el usuario `jma` y una contraseña cualquiera.

![Creación de la cuenta](./imágenes/Pasted%20image%2020260822011210.png)

Una vez autenticados accedemos al panel principal, donde aparecen distintos eventos corporativos. Lo interesante es que, además de las opciones disponibles para un usuario normal, aparece un botón **Admin dashboard**.

![Panel del usuario](./imágenes/Pasted%20image%2020260822011255.png)

Al intentar acceder al dashboard, la aplicación responde con `Access denied` e indica que se necesitan privilegios de administrador.

![Acceso denegado](./imágenes/Pasted%20image%2020260821222502.png)

Antes de analizar la sesión también probamos una alternativa sencilla: iniciar sesión directamente con el usuario `admin` utilizando a modo de prueba algunas credenciales comunes que suelen setearse por fdefecto. La aplicación respondió con `Invalid credentials`, por lo que descartamos este camino.

![Intento de login como admin](./imágenes/Pasted%20image%2020260821222731.png)

A partir de esto revisamos las cookies almacenadas por el browser. La aplicación mantiene la sesión mediante una cookie llamada `session`, el valor de esta cookie tiene la estructura típica de un **JWT (JSON Web Token)**.

![Cookie de sesión](./imágenes/Pasted%20image%2020260821225436.png)

Copiamos el token y lo decodificamos utilizando la herramienta CyberChef:

```text
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqbWEiLCJuYW1lIjoiam1hIiwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODczNjM1OTg2NDl9.SFZB8S8MArcK14lxpDSNfaVLG4RbdtK_VsgFSC_4qzs
```

El payload obtenido fue:

```json
{
  "sub": "jma",
  "name": "jma",
  "role": "user",
  "iat": 1787363598649
}
```

![JWT decodificado](./imágenes/Pasted%20image%2020260821225414.png)

El campo que más nos interesó fue:

```json
"role": "user"
```

Esto coincide con el comportamiento que habíamos visto hasta al momento, es decir, nuestra sesión pertenece a un usuario normal y el servidor no nos permite acceder al panel administrativo.

Por lo tanto, decodificar el JWT nos permitió comprobar si podíamos modificar el payload, volver a firmar el token y conseguir que la app lo aceptara.

Cambiamos entonces el rol de `user` a `admin`:

```json
{
  "sub": "jma",
  "name": "jma",
  "role": "admin",
  "iat": 1787363598649
}
```

Para generar nuevamente la firma volvemos a usar CyberChef (JWT Sign), utilizamos **HS256** y la clave `secret`.

![JWT modificado y firmado](./imágenes/Pasted%20image%2020260821225512.png)

Con el nuevo JWT generado, reemplazamos manualmente el valor de la cookie `session` del browser.

![Cookie modificada](./imágenes/Pasted%20image%2020260821225541.png)

Al recargar la aplicación seguimos autenticados como `jma`, pero ahora el servidor reconoce el valor `role: admin` incluido en nuestro token. Al volver a ingresar a **Admin dashboard**, esta vez el acceso fue permitido.

Dentro del panel administrativo encontramos finalmente la flag del reto:

```text
brunner{well_known_secret}
```

![Flag obtenida](./imágenes/Pasted%20image%2020260821225623.png)

Ingresamos la flag en la plataforma de BrunnerCTF y el reto queda resuelto correctamente.

![Reto completado](./imágenes/Pasted%20image%2020260821225742.png)