# Baby First Forensics

---

- CTF URL -> [BFF](https://play.duc.tf/challenges#Baby's%20First%20Forensics-35)

---

Enunciado 

```
They've been trying to breach our infrastructure all morning! They're trying to get more info on our covert kangaroos! We need your help, we've captured some traffic of them attacking us, can you tell us what tool they were using and its version?

NOTE: Wrap your answer in the DUCTF{}, e.g. DUCTF{nmap_7.25}
```

El punto clave del enunciado es -> what tool they were using and its version <-

---

Recurso

- [Captura de trafico](recurso/capture.pcap)

---

## Resolución

El archivo a descargar es una captura de tráfico que puede ojearse con la herramienta wireshark.

- Para ahorrarnos unos MB de descarga, también puede ejecutarse el comando `strings` - [strings command](https://www.howtogeek.com/427805/how-to-use-the-strings-command-on-linux/) - en bash para mostrar en pantalla parte del contenido.
- Una vez realizado esto, vemos el extracto 
```<h2>Error
  404</h2>
<address>
  <a href="/">
172.16.17.135</a><br />
  <span>
Thu Oct 20 04:36:38 2016<br />
Apache/2.2.8 (Linux/SUSE)</span>
</address>
</body>
</html>
GET /cgi-bin/cgiwrap/~root HTTP/1.1
Connection: Keep-Alive
User-Agent: Mozilla/5.00 (Nikto/2.1.6) (Evasions:None) (Test:000964)
Host: 172.16.17.135
m8HTTP/1.1 404 Not Found
Date: Wed, 19 Oct 2016 20:36:38 GMT
Server: Apache/2.2.8 (Linux/SUSE)
Vary: accept-language,accept-charset
Accept-Ranges: bytes
```
- Sospechamos entonces que la información requerida puede estar en el header de ``User-Agent`` y para despejar dudas, tiramos un grep sobre la salida standar del comando anterior
- ``sh`` strings capture.pcac | grep User-Agent
 ```
User-Agent: Mozilla/5.00 (Nikto/2.1.6) (Evasions:None) (Test:000479)
 ```
- Aparece repetidamente la herramienta utilizada y la version.
- Pues entonces la flag requerida resulta ser ``DUCTF{nikto_2.1.6}``

---

- Para mayor detalle mirar el archivo ``solve.sh``