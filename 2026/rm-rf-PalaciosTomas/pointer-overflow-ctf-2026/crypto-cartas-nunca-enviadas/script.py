from itertools import permutations

# Ciphertext original de la instancia que aparece en la página del reto
CIPHERTEXT = "HUROZ{2.1287.TBOI5YZWHGTGYUR6.HFQDQBOQDVYQ554R2V7ID3DPNC}"

# Palabras extraídas de los márgenes y metadatos del reto
MARGIN_WORDS = ["WILLOW", "IRIS", "ROSE", "TULIP", "ELDER", "HARP"]
THEMATIC_KEYS = ["WITHER", "WITHEROSE", "WHITMORE", "ALDOUS"]


def beaufort_decrypt(text: str, key: str) -> str:
    """Aplica el descifrado Beaufort estricto (avanza el índice de clave solo en letras)."""
    out = []
    j = 0

    for ch in text:
        if ch.isascii() and ch.isalpha():
            c = ord(ch.upper()) - ord("A")
            k = ord(key[j % len(key)].upper()) - ord("A")
            out.append(chr((k - c) % 26 + ord("A")))
            j += 1
        else:
            # Los delimitadores, puntos y números se mantienen intactos
            out.append(ch)

    return "".join(out)


def main():
    print("=== 1. PRUEBA DE PALABRAS DE LOS MÁRGENES Y COMBINACIONES ===")

    # A) Probamos palabras individuales y claves temáticas
    all_single_keys = MARGIN_WORDS + THEMATIC_KEYS
    for key in all_single_keys:
        res = beaufort_decrypt(CIPHERTEXT, key)
        if res.startswith("POCTF"): # Si el resultado comienza con "POCTF", es una coincidencia
            print(f"[+] ¡prefijo compatible! Clave candidata: '{key}'")
            print(f"    -> Flag: {res}\n")

    # B) Probamos permutaciones de a pares (p. ej. WILLOWROSE, ROSEIRIS, etc.)
    for a, b in permutations(MARGIN_WORDS, 2):
        key = a + b
        res = beaufort_decrypt(CIPHERTEXT, key)
        if res.startswith("POCTF"):
            print(f"[+] ¡Coincidencia de par encontrada! Clave: '{key}'")
            print(f"    -> Flag: {res}\n")

    print("=== 2. VERIFICACIÓN Y COMPARACIÓN DE LAS CLAVES CANDIDATAS ===")
    for key in ["WITHER", "WITHEROSE"]:
        flag = beaufort_decrypt(CIPHERTEXT, key)
        print(f"Clave: {key:<10} -> Flag: {flag}")


if __name__ == "__main__":
    main()