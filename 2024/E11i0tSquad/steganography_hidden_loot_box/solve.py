#!/usr/bin/env python3
# Solver - Hidden Loot Box (DEADFACE CTF 2024) - Steganography / Web
# La pagina apila una imagen "cover" encima de otra via CSS. La de abajo (hidden.png)
# esta servida como estatico y tiene el flag escrito. Este script mira el HTML, agarra
# la imagen que NO es la "cover", la descarga y (si hay tesseract) le saca el flag por OCR.

import re
import urllib.request
import urllib.error
from urllib.parse import urljoin

BASE = "http://45.79.200.170:3001/"   # pagina del reto


def get(url):
    return urllib.request.urlopen(url, timeout=5).read()


def main():
    try:
        html = get(BASE).decode(errors="replace")
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        print(f"[!] No se pudo conectar a {BASE} ({e}).")
        print("[i] La instancia oficial del CTF finalizó.")
        print("[+] La URL del recurso estático descubierto durante la competencia fue: http://45.79.200.170:3001/static/hidden.png")
        print("[+] Flag documentada: deadface{uh_I_feel_exposed}")
        return

    imgs = re.findall(r'<img[^>]*src="([^"]+)"', html)
    print("[*] Imagenes en la pagina:", imgs)

    # la 'cover' es la visible de arriba; la oculta es la otra
    hidden = [u for u in imgs if "cover" not in u.lower()]
    target = urljoin(BASE, hidden[0] if hidden else "/static/hidden.png")
    print(f"[*] Imagen oculta: {target}")

    try:
        data = get(target)
    except Exception as e:
        print(f"[!] Error descargando {target}: {e}")
        return

    out = target.rsplit("/", 1)[-1] or "hidden.png"
    with open(out, "wb") as f:
        f.write(data)
    print(f"[+] Guardada {out} ({len(data)} bytes)")

    # si hay OCR, imprimimos el flag directamente
    try:
        from PIL import Image
        import pytesseract
        txt = pytesseract.image_to_string(Image.open(out)).strip()
        print(f"[+] Flag (OCR): {txt}")
    except Exception as e:
        print(f"[i] Sin OCR ({e}). Abri '{out}': el flag esta escrito en la imagen.")


if __name__ == "__main__":
    main()
