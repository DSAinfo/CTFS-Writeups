# Wait For It
#### Descripción
just a pcap file
#### Adjuntos
capture.pcap
### Desarrollo
El reto plantea un escenario donde hay que hacer análisis de tráfico con el archivo adjunto que es un .pcap.

![Captura de pantalla](imagenes/Pasted image 20261027154145.png)

Casi la totalidad es IRC y hay algo de HTTP/DNS.

Filtrando en Wireshark por IRC, se observa el siguiente intercambio de mensajes:

![Captura de pantalla](imagenes/Pasted image 20261027163540.png)

![Captura de pantalla](imagenes/Pasted image 20261027163556.png)

![Captura de pantalla](imagenes/Pasted image 20261027163612.png)

![Captura de pantalla](imagenes/Pasted image 20261027163629.png)

![Captura de pantalla](imagenes/Pasted image 20261027163644.png)

![Captura de pantalla](imagenes/Pasted image 20261027163721.png)

Este conjunto de mensajes se repite una y otra vez entre los mismos hosts.

![Captura de pantalla](imagenes/Pasted image 20261027164420.png)

Posteriormente en la captura aparece otro host:

![Captura de pantalla](imagenes/Pasted image 20261027164636.png)

Si filtramos su IP, vemos que tiene su propio conjunto de mensajes que se repiten al igual que los primeros.

![Captura de pantalla](imagenes/Pasted image 20261027164752.png)

![Captura de pantalla](imagenes/Pasted image 20261027164809.png)

![Captura de pantalla](imagenes/Pasted image 20261027164821.png)

Ambas flags son falsas, pero este último deja una pista clave "the flag is in the timing".

Si observamos "el timing" de los paquetes de estos mensajes, podemos ver variaciones en ráfagas entre el tiempo y la cantidad de paquetes que se envían.
Ajustando la vista podemos obtener lo siguiente:
![Captura de pantalla](imagenes/Pasted image 20261027165619.png)

![Captura de pantalla](imagenes/Pasted image 20261027165713.png)

Esto corresponde para el flujo entre los hosts 10.13.37.7 y 192.168.1.42.
No era la flag pero podemos saber que esta bién encaminado porque vimos que estos mensajes transcurrían al mismo tiempo que el primer set y la flag falsa decía "cruXipher{d3c0y_str34m}", haciendo referencia a que es una obfuscación, un "stream señuelo".

Si aplicamos el mismo procedimiento al conjunto de mensajes de los hosts 10.13.37.7 y 192.168.1.23 obtenemos:

![Captura de pantalla](imagenes/Pasted image 20261027170813.png)

![Captura de pantalla](imagenes/Pasted image 20261027170933.png)

https://morsecode.world/international/translator.html

**Flag:** cruXipher{T1M1NG_1S_3V3RYTH1NG}
