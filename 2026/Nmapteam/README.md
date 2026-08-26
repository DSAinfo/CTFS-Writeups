# gaslightCTF 2026 — Writeups

**Grupo:** NmapTeam
**Materia:** Desarrollo Seguro de Aplicaciones (Facultad de Informática, UNLP) — Trabajo Final 2026
**Alumno:** Ventos Valentin 03208/4

## Evento

- **CTF:** gaslightCTF 2026
- **Formato:** Jeopardy-style
- **Fechas:** 14 ago 2026 12:00 UTC — 17 ago 2026 12:00 UTC (72 h)
- **Sitio:** https://gaslightctf.cooking/
- **Plataforma:** https://play.gaslightctf.cooking/
- **CTFtime:** https://ctftime.org/event/3181/
- **Formato de flag:** `gaslightCTF{[\w\-_!?]+}` (ej: `gaslightCTF{w3lc0me_2_g4sl1ghtCTF!}`)

## Retos resueltos

Según la consigna se resuelven como mínimo **3 retos**: dos de categorías relacionadas con los contenidos de la materia y uno adicional de categoría libre. No se incluyen retos warm-up / introductorios.

| # | Reto | Categoría | Puntos | Relación con la materia |
|---|------|-----------|--------|-------------------------|
| 1 | [`biscuit`](./biscuit/Writeup.md) (The Jaffa Cake Zone) | Web | 447 | A05 Injection (inyección de Datalog) + Broken Access Control |
| 2 | [`Transpose`](./transpose/Writeup.md) | Crypto | 427 | A04 Cryptographic Failures (transposición de columnas) |
| 3 | [`affine-hill`](./affine-hill/writeup_affine_hill.md) | Crypto | 422 | A04 Cryptographic Failures (known-plaintext attack sobre cifrado lineal) |
| 4 | [`messageboard`](./messageboard/Writeup.md) | Web | 497 | A05 Injection (SQLi en `ORDER BY`) + Broken Access Control |


## Estructura

Cada reto tiene su propia carpeta con:

- Write-up (`Writeup.md` / `writeup_*.md`) — análisis y proceso de resolución
- Script de resolución (`solve.py`) cuando el reto lo permite
- `recursos/` — archivos entregados por el reto (código fuente, `output.txt`, etc.), incluidos los `.tar.zst` originales para que la cátedra pueda reproducir el reto
- `imagenes/` — capturas de pantalla y evidencias del proceso

## Resumen

- **Total de retos:** 4
- **Categorías cubiertas:** Web, Crypto
- **Flags obtenidas:**
  - `biscuit`: `gaslightCTF{d3f1nit3ly_a_cak3_f0r_l3g4l_r34s0n5_5ae0911644d7}`
  - `Transpose`: `gaslightCTF{tr4nsp0s3-2-th3-k3y-0f-g-fl4t!}`
  - `affine-hill`: `gaslightCTF{kn0wn-pl41nt3xt-4tt4cks-4r3-sup3r-s1mpl3}`
  - `messageboard`: `gaslightCTF{ar3_y0u_my_cl0s3_fr13nd_n0w?_12a64ae2d59d}`

---


