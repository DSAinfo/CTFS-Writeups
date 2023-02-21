![alt text](https://i.imgur.com/Myj2SZw.png)

El reto nos provee de una captura de red bajo el nombre de ```network-dump.flag.pcap```

Podemos analizarla con Wireshark la cual nos muestra una comunicación TCP

![alt text](https://i.imgur.com/OPuFQ5p.png)

Si seguimos el flujo TCP de la comunicación podemos dar con la flag

![alt text](https://i.imgur.com/8y2CTEl.png)
![alt text](https://i.imgur.com/Kb8i5Bl.png)

Una alternativa es usar el comando tshark para dar con el resultado, usando el siguiente comando sobre la captura de tráfico:

<code>tshark -r recurso/network-dump.flag.pcap -nqz "follow,tcp,ascii,0"</code>

![alt text](https://i.imgur.com/2mhXc04.png)
