#!/bin/bash

# Paso 1: Descargamos el archivo
# Tabsspaces.zip

# Paso 2: Extraemos el contenido
unzip -q recurso/Tabsspaces.zip -d extract

# Paso 3: Calculamos los checksums y encontramos la imagen diferente
# Cambiamos al directorio donde están los archivos
cd extract/ctf/files

# Calculamos los checksums de los archivos ocultos y los guardamos en un archivo
for file in .*.jpg; do
    sha256sum "$file" >> "checksum.txt"
done

# Ordenamos y contamos los checksums únicos, luego filtramos el que aparece solo una vez
awk '{print $1 " " $2}' checksum.txt | sort | uniq -c | grep " 1 " | awk '{print $2}' > diff_checksum.txt

# Leemos el checksum único del archivo
checksum=$(cat diff_checksum.txt)

# Encontramos el nombre del archivo que corresponde a ese checksum
file_different=$(grep "$checksum" checksum.txt | awk '{print $3}')

# Paso 4: Extraemos datos ocultos de la imagen sospechosa
steghide extract -sf ". $file_different" -p "" -f

# Paso 5: Convertimos espacios y tabulaciones a binario
cat whitespace_flag.txt | sed 's/ /0/g' | sed 's/	/1/g' > binary_flag.txt

# Paso 6: Convertimos binario a ASCII
flag=$(cat binary_flag.txt | tr -d '\n' | perl -lpe '$_=pack"B*",$_')

# Paso 7: Mostramos la flag obtenida
echo "Flag obtenida: $flag"
