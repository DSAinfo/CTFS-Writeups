#!/bin/bash

# Obtener la primera linea encontrada de User-Agent
user_agent=$(strings recurso/capture.pcap | grep User-Agent | head -1)

# Utilizando awk y regex, me quedo con la parte de la linea q matchee con el standar de versionado XX.YY.zz
tool_version=$(echo "$user_agent" | awk -F '[()]' '{for(i=1;i<=NF;i++) if ($i ~ /\/[0-9]+\.[0-9]+\.[0-9]+/) print $i}')

# Lo paso a lower case pues asi lo requiere la flag
version_lower=$(echo "$tool_version" | tr '[:upper:]' '[:lower:]')

duc_flag="DUCTF{${version_lower//\//_}}"

# Escribo a archivo de texto
echo "$duc_flag" > flag.txt