# Pathcode

![picture 32](../../images/65bbbbded56eb21d61ed30d7016c6ac3955fbdd99aba5108ae1624e7da77aaef.png)  

Nos dan una IP y Puerto para conectarnos al desafio

![picture 33](../../images/7086edf1710da95f04ba275803685e8f8ded6623dc5d961be392b9555ee70cad.png)  

El desafio nos deja ingresar 2 veces un string, luego repite el codigo y al parecer lo encripta de alguna forma. No se nos proporciono el codigo fuente, ni un archivo al cual poder hacer un `objdump -t ` asi que se podria asumir que la solucion no es demasiado compleja. <br>
Como el desafio dice mucho "escape", voy a probar escapar con \n todo lo posible

![picture 34](../../images/c59d517b5d11e481422195a349f593fbd55561377fd3d534a2350d9008982fb7.png)  

Al escapar, se escapo literalmente a la consola del desafio. Por ende, buscamos la flag (que luego de buscarla, sabemos que esta en /home/ctf/flag)

 <img src="../../images/0abd733272a199f283c35e88d29fff783c55f7872788a9607ed6e1452171e896.png" alt="HTML5 Icon" style="width:70%;height:100%;"> 

![picture 35](../../images/64059b0a00791dbc48be61a72cdd247dfc45b7a2f340cbf26edd396912762d69.png)  

```
Flag: T3N4CI0US{dkf347324786efslkhaflkjhfdgdkhflkj1534fdaaf}
```