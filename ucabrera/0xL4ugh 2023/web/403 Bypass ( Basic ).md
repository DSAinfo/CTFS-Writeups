# 403 Bypass ( Basic )

### Some one reported to our Bug Bounty Program that he found a secret page that discloses some senstive information and we forbidden any access to it [link](http://20.121.121.120/secret.php)

### Author : abdoghazy
---

Si entramos a la URL, nos dice: You are forbidden!. Vemos que no tiene fuente. Probamos con curl y distintos verbos, y siempre obtenemos lo mismo, ahora si prestamos atención a la descripción del challenge, dice que habia algo, pero que ahora no está más, por lo tanto probemos con [wayback machine](https://web.archive.org/web/20230217010631/http://20.121.121.120/secret.php), vemos que existe una captura, con fecha de antes, mas bien hora, de que comience el ctf.

![Captura de wayback machine](../images/2023-02-17_193920_web.archive.org.png)

Flag: 0xL4ugh{All_The_W@@y_Up_Fr33_Palestine}