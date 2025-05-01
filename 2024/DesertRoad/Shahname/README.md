# Resumen
El desafió consiste en obtener las cookies del administrador de la pagina de una galería de fotos. Para eso se utiliza un XSS.

# Write up
El ejercicio nos presenta con la siguiente pagina:

![shanahme1.png](./images/shahname1.png)


Que al analizar el source code de los scripts de Javascript del mismo se puede encontrar una variable que no es sanitizada antes de ser utilizada.

![shanahme2.png](./images/shahname2.png)


Por lo que, si se arma un payload XSS de Javascript, se puede enviar las cookies utilizadas por el usuario a un servidor remoto.

![shanahme3.png](./images/shahname3.png)


Una vez armado el payload, este es mandado al "administrador" a través de una herramienta de "reporte".

![shanahme4.png](./images/shahname4.png)


![shanahme5.png](./images/shahname5.png)


Y de esta manera, una vez el administrador abre el link, obtenemos las cookies, y por lo tanto, la flag.

![shanahme6.png](./images/shahname6.png)

