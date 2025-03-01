#!/bin/bash

# Se descomprime el archivo files.zip y nos movemos al directorio files
unzip files.zip
cd files

# Se hace strings sobre el archivo sam.jpg, se toma la línea 12824 del resultado de strings (que de la lectura previa se sabe que posee el código Brainfuck) y se guarda en encrypted.txt
strings sam.jpg | sed -n '12824p' > encrypted.txt


# Se ejecuta brainfuck.py (script obtenido por ChatGPT para traducir Brainfuck, ya que no se encontró una herramienta para usar vía script) pasando encrypted.txt como parámetro
# Movimos el script brainfuck.py al directorio de trabajo usando el comando mv y find para buscarlo:
mv $(find / -name "brainfuck.py" 2>/dev/null | head -n 1)
python3 brainfuck.py encrypted.txt > link_drive.txt

# Se obtiene el enlace de descarga desde el txt para poder descargar el archivo
download_url=$(cat link_drive.txt)

# Como usando directamente el link obtenido, lo que se descarga es el HTML del Drive, se pidió una ayudita a ChatGPT para ver cómo descargarlo exitosamente
# Para eso, se extrae el ID del archivo de Google Drive del enlace y se arma un nuevo enlace para descarga directa
file_id=$(echo "$download_url" | grep -oP 'file/d/(\K[^/]+)')
drive_download_url="https://drive.google.com/uc?export=download&id=$file_id"
wget --no-check-certificate "$drive_download_url" -O downloaded_file

# Como el archivo descargado tiene sus Bytes invertidos de a pares, se lo pasa por hexdump (que muestra imprime en little endian, y por lo tanto, en el orden en que los Bytes deberían estar) y luego por xxd -r, guardándolo como samurai.jpg
hexdump downloaded_file | xxd -r > samurai.jpg

# La imagen samurai.jpg contiene otra imagen de un samurai, con la flag escrita en ella: apoorvctf{ByT3s_0UT_0F_0Rd3R}
