Secure Platform

Take a look at my super secure website. I only let people access the flag I hid there if they're just as secure as I am!

Author: Salma

Tags: intro

---

Entramos en la web:

![Página](../images/2023-03-02_093548_secure-platform.acmcyber.com.png)

Hacemos click en el botón: Get your flag!

![Respuesta negativa](../images/2023-03-02_093619_secure-platform.acmcyber.com.png)

Si vemos el request:

![request original](../images/Captura%20desde%202023-03-02%2009-41-04.png)

La única parte donde aparece Linux es en el header Sec-Ch-Ua-Platform, reemplazamos en dicho header a linux por: INTEGRITY-178B

![request modificado](../images/Captura%20desde%202023-03-02%2009-41-22.png)

![flag](../images/Captura%20desde%202023-03-02%2009-41-39.png)

Flag: flag{sh0uldv3_us3d_n4v1g4t0r}