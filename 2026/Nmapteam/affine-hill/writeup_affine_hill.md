# Write-Up: affine-hill

## 📌 Información General
* **Categoría:** Criptografía (Crypto)
* **Dificultad:** Media
* **Flag / Keywords:** `kn0wn-pl41nt3xt-4tt4cks-4r3-sup3r-s1mpl3`

---

## 1. Descripción del Desafío
El reto presenta un esquema de cifrado custom llamado **Affine-Hill Cipher** que combina elementos de un cifrado Afín y un cifrado de Hill operando sobre un alfabeto de 37 caracteres (`a-z`, `0-9`, `-`) en bloques de tamaño $m = 4$.

El creador del reto afirma que la combinación es inmune a ataques de texto claro conocido (*Known-Plaintext Attack* / KPA), pero el sistema sigue siendo puramente lineal y cuenta con un error de implementación en el código original.

---

## 2. Análisis de Vulnerabilidades

### A. Vulnerabilidad Lineal (KPA)
La ecuación de cifrado para cada bloque de texto plano $P_i$ (representado como un vector fila de $1 	imes 4$) y su correspondiente bloque cifrado $C_i$ es:

$$C_i \equiv P_i \cdot K + b \pmod{37}$$

Donde:
* $K$ es una matriz de $4 	imes 4$ derivada de la primera parte del keyword.
* $b$ es un vector desplazamiento de $1 	imes 4$ derivado de los últimos 4 caracteres del keyword.

Al ser una relación de transformación afín en $\mathbb{Z}_{37}$, la estructura conserva linealidad absoluta.

### B. Bug en la implementación (`encrypt.py`)
En el script original se observa la siguiente instrucción:
```python
pt_vecs = [list(map(lambda x: alphabet.index(x), pt_padded[m*i:m*(i+1)])) for i in range(n//m)]
```
Donde `n = len(pt)` toma la longitud del texto **sin aplicar padding** ($n = 61$).  
Al calcular `61 // 4 = 15`, el bucle únicamente procesa 15 bloques ($15 	imes 4 = 60$ caracteres), omitiendo el bloque final acolchado. Por esta razón, el output cifrado tiene una longitud de 60 caracteres.

---

## 3. Explotación Matemática

Para eliminar el término independiente $b$, restamos ecuaciones de bloques consecutivos:

$$(C_{i+1} - C_i) \equiv (P_{i+1} - P_i) \cdot K \pmod{37}$$

Agrupando 4 pares de diferencias linealmente independientes, construimos las matrices $\Delta P$ y $\Delta C$:

$$\Delta P = egin{pmatrix} P_1 - P_0 \ P_2 - P_1 \ P_3 - P_2 \ P_4 - P_3 \end{pmatrix}, \quad \Delta C = egin{pmatrix} C_1 - C_0 \ C_2 - C_1 \ C_3 - C_2 \ C_4 - C_3 \end{pmatrix}$$

Como $\Delta P$ es invertible en $\mathbb{Z}_{37}$, despejamos la matriz clave $K$:

$$K \equiv (\Delta P)^{-1} \cdot \Delta C \pmod{37}$$

Posteriormente, recuperamos el vector de desplazamiento $b$ sustituyendo $K$ en el primer bloque:

$$b \equiv C_0 - P_0 \cdot K \pmod{37}$$

---

## 4. Script de Solución (`solve.py`)

```python
from sympy import Matrix

alphabet = "abcdefghijklmnopqrstuvwxyz0123456789-"
l = len(alphabet) # 37
m = 4

pt = "b3w4reofbugs1ntheab0vec0de-ih4ve0nlyprov3ditc0rrectnottr13dit"
ct1 = "x3etd0vgd7z9v6bld4ba7p94s0acp-bvfjjfywypdkzuwsgah4shanrdaop4"
ct2 = "odbewk453xyc3210-mlqxley8loydmzgy0k6ok4i9qjcwx42om5au1-hqqkr"

def solve_key(pt_text, ct_text):
    get_vecs = lambda txt: [list(map(alphabet.index, txt[m*i:m*(i+1)])) for i in range(len(txt)//m)]
    
    # Tomamos los 15 bloques de 4 caracteres
    P = [Matrix(v).T for v in get_vecs(pt_text)[:15]]
    C = [Matrix(v).T for v in get_vecs(ct_text)]

    # Construimos las matrices de diferencias para eliminar 'b'
    delta_P = Matrix([P[i+1] - P[i] for i in range(4)])
    delta_C = Matrix([C[i+1] - C[i] for i in range(4)])

    # K = delta_P^(-1) * delta_C  (mod 37)
    K = (delta_P.inv_mod(l) * delta_C) % l
    
    # b = C[0] - P[0] * K  (mod 37)
    b = (C[0] - P[0] * K) % l

    # Reconstrucción de la clave en texto
    key_str = "".join(alphabet[K[r, c]] for r in range(m) for c in range(m))
    key_str += "".join(alphabet[v] for v in b)
    return key_str

kw1 = solve_key(pt, ct1)
kw2 = solve_key(pt, ct2)

print(f"Keyword 1: {kw1}")
print(f"Keyword 2: {kw2}")
print(f"Flag Completa: {kw1}{kw2}")
```

---

## 5. Resultados

* **Keyword 1:** `kn0wn-pl41nt3xt-4tt4`
* **Keyword 2:** `cks-4r3-sup3r-s1mpl3`
* **Flag Final:** `kn0wn-pl41nt3xt-4tt4cks-4r3-sup3r-s1mpl3`
