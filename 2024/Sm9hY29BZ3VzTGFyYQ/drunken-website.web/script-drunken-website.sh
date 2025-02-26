!/bin/bash

# Definir las URLs iniciales
BASE_URL="http://challenge.ctf.cybermaterial.com"
HOME_PAGE="$BASE_URL/dissssissssimpul/homepage.html"

# Descargar el código fuente de la página principal
echo "Descargando página principal..."
curl -s "$HOME_PAGE" -o homepage.html

# Extraer el enlace del botón invisible
echo "Buscando el botón invisible..."
INVISIBLE_BUTTON_URL=$(grep -oP '(?<=href=")[^"]*(?=" class="invisible-button")' homepage.html)

if [ -z "$INVISIBLE_BUTTON_URL" ]; then
    echo "Botón invisible no encontrado. Abortando."
    exit 1
fi

# Asegurarse de que el URL del botón no tenga un '/' duplicado
FULL_URL="$BASE_URL/${INVISIBLE_BUTTON_URL#/}"

# Descargar la página oculta donde se encuentra la flag
echo "Descargando página oculta: $FULL_URL"
curl -s "$FULL_URL" -o hidden_page.html

# Buscar la flag en el contenido descargado
echo "Buscando la flag..."
FLAG=$(grep -oP 'CM\{.*?\}' hidden_page.html)

if [ -z "$FLAG" ]; then
    echo "No se encontró la flag."
else
    echo "¡Flag encontrada: $FLAG!"
fi

# Limpiar los archivos temporales
rm homepage.html hidden_page.html
