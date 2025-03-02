# TP FINAL FORENSIA 2024

Desafio forensia: “Samurai's Code”. URL: [Apoorv CTF](https://apoorvctf.iiitkottayam.ac.in/challenges#Samurai%E2%80%99s%20Code-26)

### **Writeup Completo: Samurai's Code**

#### **Desafío:**

Revela el código perdido de los samuráis y desbloquea el misterio oculto dentro.

#### **Pasos:**

1. Descargamos el archivo files.zip
2. Extraemos el contenido usando
 
   ```unzip recurso/files.zip -d extract```
 
3. Cambiamos al directorio donde están los archivos con

   ```cd extract/ctf/files```
   
4. Se examinó el archivo sam.jpg con strings sam.jpg y se pudo encontrar una secuencia de datos extraños al final del archivo:
   ++++++++++[>+>+++>+++++++>++++++++++<<<<-]>>>>++++.++++++++++++..----.+++.<------------.-----------..>---------------.++++++++++++++.---------.+++++++++++++.-----------------.<-.>++.++++++++..--------.+++++.-------.<.>--.++++++++++++.--.<+.>-------.+++.+++.-------.<.>-.<.++.+++++++++++++++++++++++++.+++++++++++++.>+++++++++++++.<+++++++++++++.----------------------------------.++++++++.>+++++++++.-------------------.<+++++++.>+.<-----.+++++++++.------------.<+++++++++++++++.>>++++++++++++++++.<+++.++++++++.>-.<--------.---------.++++++++++++++++++++.>.<++.>--------------.<<+++++.>.>-----.+++++++.<<++.>--.<++.---------.++.>>+++++++++++.-------------.----.++++++++++++++++++.<<++++++++++++++++.>>--.--.---.<<--.>>+++.-----------.-------.+++++++++++++++++.---------.+++++.-------.

   Estos datos seguían un patrón parecido al de un código Brainfuck.
   
5. Se toma la línea que posee este código y lo guardamos en encrypted.txt

   ```strings sam.jpg | sed -n '12824p' > encrypted.txt```
   
6. Traducimos lo obtenido con brainfuck.py pasando como parámetro encrypted.txt.

   ```python3 /home/kali/Documents/CTFs/ApoorvCTF/Forensics/"Samurai’s Code"/brainfuck.py encrypted.txt > link_drive.txt```
   
    Esto nos da un link de google drive que guardamos en link_drive.txt y que contiene lo siguiente:          

   https://drive.google.com/file/d/1JWqdBJzgQhLUxLTwLCWwYi2Ydk4W6-/view?usp=sharing

   
7. Se debieron ejecutar algunos comandos para poder obtener el ID del link del drive para poder ingresar y descargar lo que contiene la URL.

   ```file_id=$(echo "$download_url" | grep -oP 'file/d/(\K[^/]+)')```
 
   ```drive_download_url="https://drive.google.com/uc?export=download&id=$file_id"```

   ```wget --no-check-certificate "$drive_download_url" -O downloaded_file```

8. Pudimos identificar que el archivo que se descarga tiene los bits invertidos por lo tanto se pasa por hexdump y luego xxd.

    ```hexdump downloaded_file | xxd -r > samurai.jpg```

12. De esta manera obtenemos otra imagen que a la izquierda de la misma se ve la flag.


#### **Flag obtenida:**
apoorvctf{ByT3s_0UT_0F_0Rd3R}
