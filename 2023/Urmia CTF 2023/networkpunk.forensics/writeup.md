![img_1](https://github.com/emilianosecchi/CTFS-Writeups/assets/49136614/8b66e9d3-9b17-4973-b739-58eee5944809)

Descargamos la captura y la analizamos con Wireshark. Empezamos observando los distintos protocolos que aparecían en la captura (TCP con TLS, SSDP e ICMP). Después descubrimos que todas las IP que aparecían eran resueltas hacia la misma máquina, porque en capa 2, todas informaban loopback. 
Igualmente, este dato no fue importante para la resolución. Luego comenzamos a revisar si encontrábamos algo de información que pudiera leerse en los bytes que contenían los campos data de los paquetes TCP, para lo que utilizamos el filtro: data.data matches "(?i)flag". 

Este nos devolvió algunos paquetes que formaban parte del tcp stream con indice 8:

![img_2](https://github.com/emilianosecchi/CTFS-Writeups/assets/49136614/7817b666-6769-4fff-9c92-396f6b057c11)

A continuación seguimos la conversación TCP y pudimos ver la siguiente data:

Hi there. Welcome to UCTF server. Give the correct command and I will expose flag to you!
showflag
For getting the flag, be more polite sir!
OK. give me flag!
200 OK. I've got your data [17 bytes]!
showflag
For getting the flag, be more polite sir!
would you please give me the flag?
For sure. Here is the flag:

![img_3](https://github.com/emilianosecchi/CTFS-Writeups/assets/49136614/c069416d-c2ed-4106-83f7-fb5df1415768)

Exportando los bytes de data del paquete pudimos identificar el flag rápidamente. El archivo exportado con el flag se puede ver dentro del directorio actual con el nombre: 'stream8_exported_data'.

![img_4](https://github.com/emilianosecchi/CTFS-Writeups/assets/49136614/e67625e7-664e-4901-8044-8f192c253f70)
