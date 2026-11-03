#!/usr/bin/env python3

import os
import sys

QUERY = "SELECT mrn FROM aurora_ehr.patients WHERE is_vip = 1;"

HOST = os.environ.get("AURORA_HOST", "aurora-mysql")
PORT = int(os.environ.get("AURORA_PORT", "3306"))
USER = os.environ.get("AURORA_USER", "player")
PASSWORD = os.environ.get("AURORA_PASS", "")


def main():
    try:
        import pymysql
    except ImportError:
        sys.exit("Falta pymysql -> pip install pymysql")

    try:
        conn = pymysql.connect(host=HOST, port=PORT, user=USER,
                               password=PASSWORD, connect_timeout=10)
    except Exception as e:
        print(f"No se pudo conectar ({e}).")
        print(f"Corre esta query en la terminal del reto:\n  {QUERY}")
        return

    with conn.cursor() as cur:
        cur.execute(QUERY)
        rows = cur.fetchall()
    conn.close()

    if not rows:
        print("No hay ningun paciente con is_vip = 1")
        return

    mrn = rows[0][0]
    print(f"Paciente VIP -> MRN: {mrn}")
    print(f"deadface{{{mrn}}}")


if __name__ == "__main__":
    main()
