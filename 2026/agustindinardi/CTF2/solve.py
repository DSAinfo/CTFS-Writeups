#!/usr/bin/env python3
import os
import re

def solve():
    resource_path = os.path.join(os.path.dirname(__file__), 'recursos', 'message.txt')

    with open(resource_path, 'r', encoding='utf-8') as f:
        ciphertext = f.read().strip()

    # Mapeo de sustitucion completo

    substitution_map = {
        # Minusculas
        'a': 'd', 'b': 'u', 'c': 'i', 'd': 'g', 'e': 'f',
        'f': 'r', 'g': 'm', 'h': 'o', 'i': 't', 'j': 'b',
        'k': 'n', 'l': 'x', 'm': 'a', 'n': 'e', 'o': 'k',
        'p': 'x', 'q': 'p', 'r': 'y', 's': 'h', 't': 's',
        'u': 'c', 'v': 'q', 'w': 'w', 'x': 'l', 'z': 'v',
        
        # Mayusculas 
        'U': 'C', 'I': 'T', 'E': 'F',
        'K': 'N', 'F': 'R', 'G': 'M', 'R': 'Y',
        'A': 'D', 'B': 'U'
    }

    plaintext_chars = []
    for char in ciphertext:
        if char in substitution_map:
            plaintext_chars.append(substitution_map[char])
        else:
            plaintext_chars.append(char)

    plaintext = "".join(plaintext_chars)

    print("[+] Mensaje descifrado correctamente:\n")
    print(plaintext)
    print("\n" + "="*50)

    match = re.search(r'picoCTF\{[^}]+\}', plaintext)
    if match:
        print(f"[+] FLAG ENCONTRADA: {match.group(0)}")
    else:
        print("[-] No se pudo aislar el formato de la flag automaticamente.")

if __name__ == "__main__":
    solve()