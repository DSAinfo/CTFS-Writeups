# CTF Writeups — Desarrollo Seguro de Aplicaciones

**Autor:** Majoros, Lorenzo (03296/1) · lorenzomajoros@alu.ing.unlp.edu.ar

**Materia:** Desarrollo Seguro de Aplicaciones — Facultad de Informática, UNLP

**Evento:** [Pointer Overflow CTF](https://pointeroverflowctf.com/)

---

## Retos resueltos

| Reto                  | Categoría | Vulnerabilidades (OWASP Top 10 2025)                              | Carpeta                                                |
| --------------------- | --------- | ---------------------------------------------------------------- | ------------------------------------------------------ |
| The Logic Inside      | Web       | A01 Broken Access Control (SSRF), A02 Security Misconfiguration   | [`The_Logic_Inside`](The_Logic_Inside)         |
| The Shape of Query    | Web       | A01 Broken Access Control, A06 Insecure Design                   | [`The_Shape_of_Query`](The_Shape_of_Query)     |
| No Structure Required | Web       | A05 Injection (NoSQL), A01 Broken Access Control, A02 Authentication Failures | [`No_Structure_Required`](No_Structure_Required) |

---

## Estructura del repositorio

```
.
├── README.md
├── No_Structure_Required
│   ├── images/                 # capturas
│   ├── solve.py                # automatización de la inyección y acceso
│   └── writeup.md              # análisis y resolución paso a paso. NoSQL Injection.
├── The_Logic_Inside
│   ├── images/                 # capturas
│   ├── script.py               # automatización de la recuperación del nonce
│   └── writeup.md              # análisis y resolución paso a paso. Recuperar el NONCE. 
└── The_Shape_of_Query
    ├── images/                 # capturas
    ├── solve.py                # automatización de las queries de acceso
    └── writeup.md              # análisis y resolución paso a paso. GraphQL.
```

Cada reto resuelto se encuentra en su propia carpeta con el write-up, el script y una subcarpeta `images/` con las capturas de pantalla.

