# Challenge Name : Giffy

- Challenge owner : Damncon2022
- Release date : 2022-12-04 12:49:42
- Dificuilty : EASY
- Points : 50
- Resource : ![Un .gif](../images/Giffy.gif)
- Description : There is no need of description. Giffy is the solution.

---

Podemos ver que es un .gif, algo pesado 8MB, que es una imagen que muestra números, los cuales parecen ser ascii, pero van muy rápido como para anotarlos, pasemos el gif a imagenes y tratemos de armar el texto.

Usamos https://convertio.co para pasar el .gif a un conjunto de .png, bajamos el zip y descomprimimos, pasamos cada numero que aparece en cada imagen a cybercheff: https://gchq.github.io/CyberChef/#recipe=From_Octal('Space')&input=MTQ0IDE0MSAxNTUgMTU2IDE0MyAxNTcgMTU2IDE3MyAxNDcgMTUxIDE0NiAxMzcgMTQzIDE2MiAxNDEgMTQzIDE1MyAxNDUgMTQ0IDE3NQ y en octal se forma la flag:
damncon{gif_cracked}