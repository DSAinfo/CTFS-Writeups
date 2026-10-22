# Cartas nunca enviadas — Letters Never Sent

**CTF:** Pointer Overflow CTF 2026  
**Categoría:** Criptografía  
**Dificultad:** Media

## 1. Descripción del reto

El desafío presenta una carta de estilo victoriano, fechada en noviembre de 1887 y dirigida al almirante Sir Francis Beaufort. En el texto se menciona un *reciprocal tableau*, lo que da una pista sobre el cifrado utilizado.

El criptograma proporcionado es:

`HUROZ{2.1287.TBOI5YZWHGTGYUR6.HFQDQBOQDVYQ554R2V7ID3DPNC}`

El objetivo es encontrar la clave escondida en las pistas del documento y recuperar la bandera.

## 2. Análisis del cifrado

La referencia a Beaufort y al *reciprocal tableau* apunta al cifrado Beaufort clásico.

Para descifrarlo, se puede utilizar la siguiente operación:

P=(K-C) mod 26

## 3. Análisis de las pistas y diccionarios de prueba

En el borde de la carta aparecen varias palabras impresas, algunas marcadas con estrellas rojas:
- **Arriba:** `WILLOW`, `IRIS`
- **Izquierda:** `ROSE`
- **Derecha:** `TULIP`
- **Abajo:** `ELDER`, `HARP`

Inicialmente probé combinaciones directas entre estas palabras de los márgenes mediante un script en Python (por ejemplo, concatenando pares como `WILLOWROSE`), pero ninguna arrojó el resultado esperado por la plataforma.

Para resolver esto, armé un pequeño conjunto de palabras candidatas (un diccionario de prueba basado en variaciones temáticas y términos del contexto del relato, como el título *Letters Never Sent* y el estado de la carta). Entre las opciones derivadas incluí la palabra `WITHER`.

También tuve en cuenta el apellido WHITMORE, que aparece en el documento. Al analizar sus letras, observé que era posible formar WITHER reordenando algunas de ellas. Por la temática de la carta, decidí probarla como clave candidata.

## 4. Pruebas realizadas

Para comprobar la hipótesis, implementé en Python el descifrado Beaufort clásico. La función avanza el índice de la clave únicamente cuando encuentra una letra y conserva los números y signos de puntuación del criptograma.

```python
def beaufort_decrypt(ciphertext, key):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    ciphertext = ciphertext.upper()
    key = key.upper()
    plaintext = []
    key_index = 0

    for char in ciphertext:
        if char in alphabet:
            k_val = alphabet.index(key[key_index % len(key)])
            c_val = alphabet.index(char)
            p_val = (k_val - c_val) % 26
            plaintext.append(alphabet[p_val])
            key_index += 1
        else:
            plaintext.append(char)

    return "".join(plaintext)

ct = "HUROZ{2.1287.TBOI5YZWHGTGYUR6.HFQDQBOQDVYQ554R2V7ID3DPNC}"
print(beaufort_decrypt(ct, "WITHER"))

```
El script devolvió la bandera correcta:

"POCTF{2.1287.YVUL5JFVPCABGXF6.BORBBVUDEJTG554R2Y7ZB3OHVR}"

### 5.Conclusión
El reto combina el análisis de pistas contextuales con la implementación del cifrado Beaufort en Python. A partir de la temática de la carta y de las palabras botánicas de los márgenes, probé las claves WITHER y WITHEROSE. Finalmente, WITHER fue la única de las dos que permitió obtener una bandera aceptada por la plataforma del CTF.