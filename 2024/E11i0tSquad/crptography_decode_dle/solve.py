#!/usr/bin/env python3
# Solver - DECODE-DLE (DEADFACE CTF 2024) - Crypto / puzzle de logica
# "Crack the code": deducir el codigo de 3 digitos a partir de 5 pistas tipo Mastermind.
# Fuerza bruta sobre los 1000 codigos (000-999) y se queda con el que cumple TODAS las pistas.

from itertools import product

# cada pista: (intento, correctos_bien_ubicados, correctos_mal_ubicados)
#   "correcto"     = el digito esta en el codigo
#   "bien ubicado" = ademas esta en esa misma posicion
CLUES = [
    ("863", 0, 1),   # One number is correct but in the wrong place
    ("250", 0, 0),   # Nothing is correct
    ("168", 0, 2),   # Two numbers are correct but in the wrong place
    ("735", 1, 0),   # One number is correct and in the right place
    ("687", 0, 2),   # Two numbers are correct but in the wrong place
]


def matches(code, guess, right, wrong):
    rp = sum(c == g for c, g in zip(code, guess))          # bien ubicados
    total = sum(min(guess.count(d), code.count(d)) for d in set(guess))  # correctos en total
    wp = total - rp                                        # correctos mal ubicados
    return rp == right and wp == wrong


def main():
    sols = ["".join(d) for d in product("0123456789", repeat=3)
            if all(matches("".join(d), g, r, w) for g, r, w in CLUES)]
    print("[*] Codigos que cumplen todas las pistas:", sols)
    if len(sols) == 1:
        print(f"[+] Codigo: {sols[0]}")
        print(f"deadface{{{sols[0]}}}")


if __name__ == "__main__":
    main()
