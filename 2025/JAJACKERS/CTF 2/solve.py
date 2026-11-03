#!/usr/bin/env python3

ciphertext = "YATLI{2.570.LNFNJOSSNETRURK7.QB6CVCXISUXTDBRYMP2NDIMHOM}"
key = "NOVENA"


def beaufort_decrypt(ciphertext: str, key: str) -> str:
    result = []
    key_index = 0

    for char in ciphertext:
        if char.isalpha():
            c = ord(char.upper()) - ord("A")
            k = ord(key[key_index % len(key)].upper()) - ord("A")

            # Beaufort clásico: P = (K - C) mod 26
            p = (k - c) % 26

            result.append(chr(p + ord("A")))
            key_index += 1
        else:
            # Conservamos números y símbolos sin modificar.
            result.append(char)

    return "".join(result)


if __name__ == "__main__":
    flag = beaufort_decrypt(ciphertext, key)
    print(flag)
