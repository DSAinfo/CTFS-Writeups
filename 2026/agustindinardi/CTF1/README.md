# No FA

## Información del reto

- **CTF:** picoCTF 2026
- **Challenge:** No FA
- **Categoría:** Web Exploitation
- **Dificultad:** Medium
- **Autor:** Darkraicg492

## Descripción

El desafío presenta una aplicación web vulnerable que utiliza autenticación mediante usuario y contraseña y, para el usuario `admin`, un segundo factor de autenticación mediante un código OTP.

El objetivo es obtener la flag accediendo como administrador.

## Archivos

- `Writeup.md`: explicación paso a paso de la resolución.
- `solve.py`: script utilizado para automatizar la explotación.
- `recursos/app.py`: código fuente proporcionado por el desafío.
- `recursos/users.db`: base de datos filtrada proporcionada por el desafío.

## Flag

```text
picoCTF{n0_r4t3_n0_4uth_3e4cf476}