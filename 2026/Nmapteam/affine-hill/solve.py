from sympy import Matrix
from math import ceil

alphabet = "abcdefghijklmnopqrstuvwxyz0123456789-"
l = len(alphabet) # 37
m = 4

pt = "b3w4reofbugs1ntheab0vec0de-ih4ve0nlyprov3ditc0rrectnottr13dit"

# Textos cifrados del output
ct1 = "x3etd0vgd7z9v6bld4ba7p94s0acp-bvfjjfywypdkzuwsgah4shanrdaop4"
ct2 = "odbewk453xyc3210-mlqxley8loydmzgy0k6ok4i9qjcwx42om5au1-hqqkr"

def get_vectors(text):
    return [list(map(lambda x: alphabet.index(x), text[m*i:m*(i+1)])) for i in range(len(text)//m)]

def solve_key(pt_text, ct_text):
    P_vecs = get_vectors(pt_text)[:15] # Tomamos los 15 bloques procesados
    C_vecs = get_vectors(ct_text)

    # Convertimos a Matrices de SymPy
    P = [Matrix(v).T for v in P_vecs]
    C = [Matrix(v).T for v in C_vecs]

    # Tomamos 4 bloques independientes para formar sistemas de ecuaciones
    # Usamos las diferencias P[i+1] - P[i] para eliminar 'b'
    delta_P = Matrix([P[i+1] - P[i] for i in range(4)])
    delta_C = Matrix([C[i+1] - C[i] for i in range(4)])

    # K = delta_P^(-1) * delta_C  (mod 37)
    K = (delta_P.inv_mod(l) * delta_C) % l

    # b = C[0] - P[0]*K  (mod 37)
    b = (C[0] - P[0] * K) % l

    # Reconstruir el keyword original
    # K está formado por m bloques de m caracteres + b de m caracteres
    keyword_chars = []
    for row in range(m):
        for col in range(m):
            keyword_chars.append(alphabet[K[row, col]])
    
    for val in b:
        keyword_chars.append(alphabet[val])

    return "".join(keyword_chars)

kw1 = solve_key(pt, ct1)
kw2 = solve_key(pt, ct2)

print(f"[+] Keyword 1: {kw1}")
print(f"[+] Keyword 2: {kw2}")