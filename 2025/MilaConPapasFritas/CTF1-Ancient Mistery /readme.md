# CTF Ancient Mystery
Url del ctf: https://kashictf.iitbhucybersec.in/challenges#Ancient%20Mystery-4

Date 03 April, 12:00 UTC — 04 April 2026, 12:00 UTC

Es un desafio de Cryptography
<img width="482" height="589" alt="Screenshot_294" src="https://github.com/user-attachments/assets/b7355d69-6514-44d8-8a58-ecd0f5ac0115" />
## Entendiendo el reto
El enunciado dice:

* Un mensaje secreto desde la epoca del Mahabharata(3136 a.C)
* Cada 64 años se recodifica el mensaje
* Han pasado 3136 años hasta la era comun
* 3136 / 64 = 49 ciclos de recodificacion
* El formato de la flag debe ser kashiCTF{...}
* Un archivo de texto “secret_message.txt”
## Analisis del archivo descargado
El archivo secret_message.txt contiene una cadena muy larga que comienza con:
Vm0wd2QyUXlVWGxWV0d4V1YwZDRWMVl3WkRSV01WbDNXa1JTVjAxV2JETlhhMUp…

* Solo contiene letras  mayusculas y minusculas
* Estructura típica de Base64
* Al decodificar una vez, se obtiene otra cadena similar, lo que indica multiples capas
## Proceso de decodificacion
Si cada 64 años se aplicaba una codificación Base64, tras 49 ciclos tendriamos 49 capas de Base 64

Solución implementada en Python:
<img width="515" height="407" alt="Screenshot_292" src="https://github.com/user-attachments/assets/663c881e-a364-4a94-a074-694dd0f4c3ef" />
## Resultado
Al ejecutar el script, despues de varias decodificaciones (49 veces), se obtiene un texto que comienza con flag{..}
<img width="418" height="180" alt="Screenshot_293" src="https://github.com/user-attachments/assets/48604383-ad2b-4dfb-937b-44fe45633612" />

La flag aparece como flag{th3…} se tiene que cambiar el prefijo por kashiCTF{..} ya que lo dice el enunciado por lo que queda
**kashiCTF{th3_s3cr3t_0f_mah4bh4r4t4_fr0m_3136_BCE}**

