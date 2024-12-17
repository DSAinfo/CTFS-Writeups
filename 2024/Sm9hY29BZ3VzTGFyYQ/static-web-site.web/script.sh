#!/bin/bash

# URL de la página principal
url="http://159.223.147.88"

# Obtener los enlaces de los archivos CSS
css_urls=$(curl -s $url | grep -oP 'href="([^"]*\.css[^"]*)"' | awk -F'"' '{print $2}')

# Verificamos si encontramos algún CSS
if [ -z "$css_urls" ]; then
    echo "No se encontraron archivos CSS."
    exit 1
fi

# Recorremos cada enlace de CSS encontrado
for css_url in $css_urls; do
    # Si el enlace es relativo, lo hacemos absoluto
    if [[ ! "$css_url" =~ ^http ]]; then
        css_url="${url}/${css_url}"
    fi
    
    echo "Comprobando archivo CSS: $css_url"
    
    # Obtener el archivo CSS y buscar la flag
    flag=$(curl -s "$css_url" | grep -oP "(?<=\/\*).*?(?=\*\/)" | grep -i "flag")
    
    # Si encontramos la flag, la mostramos y terminamos
    if [ -n "$flag" ]; then
        echo "¡Flag encontrada! $flag"
        exit 0
    fi
done

echo "No se encontró la flag en los archivos CSS."
