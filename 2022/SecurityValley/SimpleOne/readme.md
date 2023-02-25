# Writeup: Solución al challenge SecurityValley - Simple One

Este es un reto de CTF en el que tenemos que encontrar un archivo dentro de un servidor web.

## Paso 1: Inspección inicial
Accedemos a la url brindada por el reto https://pwnme.org/ y vemos que es una página simple.

## Paso 2: Inspección del recurso con Zap (Zed Attack Proxy)
Se eligió trabajar con Zap, una herramienta gratuita y de código abierto para pruebas de penetración que funciona como 'men-in-the-middle' para testear aplicaciones web.

Como primer paso de inspección del recurso, se realizó un escaneo automático que brinda un Spider y Ajax Spider: herramientas para escaneo automático, permitiendo además descubrir contenido dinámico en el segundo caso (como contenido generado por JS o Ajax). De esta inspección se pudo obtener el siguiente árbol de contenidos:

A partir del árbol encontrado, se utilizó la herramienta de fuerza bruta (forced browse) que provee Zap para descubrir directorios accesibles en el servidor web que aloja al recurso. Zap provee un listado básico de directorios posibles 'directory-list-1.0.txt'.

## Paso 3: Inspección de los resultados obtenidos

La primer petición exitosa que podemos ver agregada a nuestro árbol de contenidos es hacia la ruta /s. Inspeccionamos la respuesta, pero vemos que tiene el html del recurso incluído en la ruta raíz.

Continúa corriendo la herramienta forced browse, y nuevamente obtenemos una nueva ruta /toolkits. Al inspeccionar la respuesta, finalmente nos encontramos con la flag requerida para resolver el challenge.

## Conclusión
En resumen, la solución al challenge SecurityValley - Simple One involucró la inspección del árbol de rutas contenido dentro del recurso brindado y la utilización de la herramienta de fuerza bruta provista por el software de pentesting ZAP para descubrir directorios dentro del servidor web y finalmente, encontrar el recurso "perdido".
