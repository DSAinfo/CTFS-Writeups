# Writeup: Solución al challenge SecurityValley - Simple One

Este es un reto de CTF en el que tenemos que encontrar un archivo dentro de un servidor web.

![challengeSO](https://user-images.githubusercontent.com/34712618/221376136-d33dcaa2-8029-4cdc-a0af-4eaaaa0fd8e3.png)

## Paso 1: Inspección inicial
Accedemos a la url brindada por el reto https://pwnme.org/ y vemos que es una página simple.

## Paso 2: Inspección del recurso con Zap (Zed Attack Proxy)
Se eligió trabajar con Zap, una herramienta gratuita y de código abierto para pruebas de penetración que funciona como 'men-in-the-middle' para testear aplicaciones web.

Como primer paso de inspección del recurso, se realizó un escaneo automático que brinda un Spider y Ajax Spider: herramientas para escaneo automático, permitiendo además descubrir contenido dinámico en el segundo caso (como contenido generado por JS o Ajax). De esta inspección se pudo obtener el siguiente árbol de contenidos:

![arbol challenge](https://user-images.githubusercontent.com/34712618/221376279-df6a32dd-4474-428f-b5c4-1e0d5fc4708a.png)

Hasta aquí, no se encontró ningún recurso asociado con la resolución del challenge. 

Por lo que, a partir del árbol encontrado, se elige utilizar la herramienta de fuerza bruta (forced browse) que provee Zap para descubrir directorios accesibles en el servidor web que aloja al recurso. Zap también provee un listado básico de directorios posibles 'directory-list-1.0.txt'.

## Paso 3: Inspección de los resultados obtenidos

La primer petición exitosa que podemos ver agregada a nuestro árbol de contenidos es hacia la ruta /s. Inspeccionamos la respuesta, pero vemos que tiene el html del recurso incluído en la ruta raíz:

![file s](https://user-images.githubusercontent.com/34712618/221376111-c8329aa7-02f3-4d42-8960-87ceef286ffa.png)

Continúa corriendo la herramienta forced browse, y nuevamente obtenemos una nueva ruta /toolkits. Al inspeccionar la respuesta, finalmente nos encontramos con la flag requerida para resolver el challenge:

![flag challenge](https://user-images.githubusercontent.com/34712618/221376119-a64a1014-8c99-49ee-a123-8275af1fed65.png)

## Conclusión
En resumen, la solución al challenge SecurityValley - Simple One involucró la inspección del árbol de rutas contenido dentro del recurso brindado y la utilización de una herramienta de fuerza bruta para descubrir directorios dentro del servidor web y, finalmente, encontrar el recurso "perdido".
