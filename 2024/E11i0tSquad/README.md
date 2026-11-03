# Desarrollo Seguro de Aplicaciones — Trabajo Final

Writeups del grupo **E11i0tSquad**. Los retos resueltos corresponden al **DEADFACE CTF 2026** (organizado por Cyber Hacktics), con sus respectivos writeups y scripts de resolución.

## Integrantes

- Lorenzo Repetto - `15143/5`
- Ramiro Gutierrez Paulos — `19136/4`

## Equipo

E11i0tSquad

## Repositorio de la cursada

https://github.com/DSAinfo/2024-E11i0tSquad

## Datos del evento

- Nombre: **DEADFACE CTF 2026**
- CTFtime: https://ctftime.org/event/2443
- Página oficial: https://ctf.deadface.io/
- Fechas del evento: 18/10/2026 – 20/10/2026

Los retos se resolvieron sobre las instancias provistas (por ejemplo `http://45.79.200.170:3000/`, `aurora.dctf.io` y `http://45.79.200.170:3001/`).

## Retos resueltos

| Reto | Categoría | Tipo de Requisito | Writeup & Script |
|--|--|--|--|
| [Health Spark – Login Information Disclosure](./deadface_login_bypass/writeup.md) | Web | Relacionado con la temática (Web) | [`writeup.md`](./deadface_login_bypass/writeup.md) / [`solve.py`](./deadface_login_bypass/solve.py) |
| [Admitted Under Another Name](./admitted_under_another_name/writeup.md) | Web (Database / SQL) | Relacionado con la temática (Web) | [`writeup.md`](./admitted_under_another_name/writeup.md) / [`solve.py`](./admitted_under_another_name/solve.py) |
| [Hidden Loot Box](./steganography_hidden_loot_box/writeup.md) | Web (Stego / Exposición de estáticos) | Relacionado con la temática (Web) | [`writeup.md`](./steganography_hidden_loot_box/writeup.md) / [`solve.py`](./steganography_hidden_loot_box/solve.py) |
| [DECODE-DLE](./crptography_decode_dle/writeup.md) | Cryptography / Logic | Categoría libre (a elección) | [`writeup.md`](./crptography_decode_dle/writeup.md) / [`solve.py`](./crptography_decode_dle/solve.py) |

## Estructura del directorio

Cada reto se encuentra organizado en su propia carpeta con su documentación, evidencias y script automático:

```text
2024/E11i0tSquad/
├── README.md
├── deadface_login_bypass/
│   ├── writeup.md
│   ├── solve.py
│   └── images/
├── admitted_under_another_name/
│   ├── writeup.md
│   ├── solve.py
│   └── images/
├── steganography_hidden_loot_box/
│   ├── writeup.md
│   ├── solve.py
│   └── images/
└── crptography_decode_dle/
    ├── writeup.md
    ├── solve.py
    └── images/
```

## Reproducción de scripts

Cada reto contiene un script `solve.py` ejecutable en Python 3:

```bash
# Health Spark
cd deadface_login_bypass && python3 solve.py

# Admitted Under Another Name
cd ../admitted_under_another_name && python3 solve.py

# Hidden Loot Box
cd ../steganography_hidden_loot_box && python3 solve.py

# DECODE-DLE
cd ../crptography_decode_dle && python3 solve.py
```
