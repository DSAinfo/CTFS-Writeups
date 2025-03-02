#!/bin/bash

# Paso 1: Extraer el archivo Brokenfr.7z previamente descargado
7z x recurso/Brokenfr

# Paso 2: Navegar al directorio extraído
cd _

# Paso 3: Navegar a la carpeta donde está el archivo sospechoso
cd word/media

# Paso 4: Renombrar el archivo sospechoso a formato PNG
cp not_so_suspicious_file suspicious.png

# Paso 5: Arreglar la cabecera del archivo PNG
printf "\x89PNG\r\n\x1a\n" | dd of=suspicious.png bs=1 conv=notrunc

# Paso 6: Abrir la imagen reparada
xdg-open suspicious.png
