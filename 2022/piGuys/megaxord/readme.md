# Writeup: Solución al challenge BuckeyeCTF 2022 - megaxord

Reto CTF de criptografía en el que nos dan un .txt y tenemos que descifrar el flag:

![image](https://user-images.githubusercontent.com/11562125/232357856-22045174-5141-48e3-a154-9a360d954a6c.png)

## Solución:

Al abrir el archivo vemos que el contenido está encriptado:

![image](https://user-images.githubusercontent.com/11562125/232358283-3ed9f1ff-3937-49bc-a366-a25eea45713c.png)
*extracto de megaxord.txt*

Debido al nombre del reto (mega'XOR'd) suponemos que se trata de una encriptación utilizando XOR, entonces para desencriptar el texto, utilizamos la herramienta CyberChef.
Al no saber la key del XOR ni su formato, decidimos utilizar la operación magic. La operación Mágica intenta detectar varias propiedades de los datos de entrada y sugiere qué operaciones podrían ayudar a darle más sentido.
El resultado es fallido en un primer intento:

![image](https://user-images.githubusercontent.com/11562125/232359240-45dd971f-b032-453f-98ce-84e5b252a46e.png)

Por lo tanto activamos el modo intensivo y obtenemos lo siguiente:

![image](https://user-images.githubusercontent.com/11562125/232358166-9c52d522-6086-4424-ba03-8c7deb977fb6.png)

Vemos el texto desencriptado pareciendo ser la copia del texto del artículo de los Power Rangers tomado de Wikipedia:

![image](https://user-images.githubusercontent.com/11562125/232359583-765f9bc8-edc2-4757-ba1e-4b71a3cfad0c.png)
*extracto de megaxord_decypted.txt*

Por último leyendo el texto encontramos casi al final el flag:

![image](https://user-images.githubusercontent.com/11562125/232360010-7af3cd89-0511-44b6-bcd6-f1a106c3d3cc.png)

Al ingresar este flag en el reto, nos la tomó como valida, dándonos 60pts en BuckeyeCTF 2022.

## Flag

`buckeye{m1gh7yxm0rph1nxw1k1p3d14xp4g3}`

## Conclusión

Nos parece un reto interesante a la hora de calentar motores en lo que a la resolución de CTF's respecta y entretenido al ser un reto de criptografía en donde utilizamos la herramienta CyberChef. 

*Enlace: https://pwnoh.io/*
