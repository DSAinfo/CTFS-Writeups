# X-Ray Vision
## Categoría: Web
### Tenemos el siguiente enunciado:
<img width="521" height="530" alt="criptoenun" src="https://github.com/user-attachments/assets/77428f4c-1099-4af4-a6c9-cf11dc1c22e7" />

### La traducción es : “Nuestro equipo de vigilancia interceptó una transmisión desde el interior de la red TradeVisor. El agente utilizó un cifrado para proteger el mensaje. Decodificalo, recupera la clave de acceso y envíala para desbloquear la bóveda.”
### Además nos proporciona un archivo .txt con el mensaje.
### Observando el texto que aparece en el archivo, sospechamos de que podría estar cifrado con algún tipo de rot, probando obtenemos con rot47 el siguiente texto:
<img width="1342" height="726" alt="rot47" src="https://github.com/user-attachments/assets/f7fb7f40-91f0-4287-bbb5-15a3796d06bc" />

### Como vemos todavía no obtenemos la flag , pero si otra pista: el segundo mensaje también está cifrado en algún tipo de rot. 
### Si aplicamos rot13 sobre el texto anterior 
<img width="1083" height="495" alt="rot13" src="https://github.com/user-attachments/assets/441b0beb-1edc-400f-afe6-dff76e6a5f28" />

### Finalmente obtenemos la flag : jctf{4cbdcC0Dc=FEbd0J_F}
### Ejecutando el script solve.py se obtiene la flag de manera automatica.
