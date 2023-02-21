![alt text](https://i.imgur.com/HEmfMUy.png)

El reto nos provee una imagen de disco comprimida  ```disk.img.gz``` y nos propone sacar el tamaño de la partición del sistema Linux.

Para esto debemos conectarnos por netcat a un servidor y proveer la respuesta

Primero descomprimimos el archivo con
<code>gzip -d disk.img.gz</code>

Con el commando <code>mmls</code> podemos ver la información de la imagén de disco. La cual podemos ver que es **0000202752**
![alt text](https://i.imgur.com/tEexX7w.png)

Nos conectamos por netcat y enviamos el valor, dandonos la flag como respuesta.

![alt text](https://i.imgur.com/WbnQodE.png)

Adicionalmente podemos directamente ingresar el valor a netcat con el siguiente comando:

<code>echo 000202752 | nc saturn.picoctf.net 52279</code>

