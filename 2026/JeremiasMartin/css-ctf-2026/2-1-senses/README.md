# 2(-1) Senses

**CTF:** [CSS CTF 2026: Return of Nexus](https://ctftime.org/event/3434)  
**Categoría:** Esteganografía  
**Dificultad:** Fácil  
**Fecha de resolución:** 30/09/2026  
**Reto:** 2(-1) Senses

![Portada evento](./imágenes/Pasted%20image%2020261001152746.png)

![Enunciado](./imágenes/Pasted%20image%2020261001170147.png)

El reto nos provee inicialmente de un archivo de audio llamado `2senses_puzzle.wav`. La descripción del reto habla acerca de un "sonido procedente del espacio profundo que, luego de intentar descifrarlo, parece aludir a nosotros". Además nos da una advertencia respecto del volumen a la hora de reproducirlo.

Tanto el nombre del reto, **2(-1) Senses**, como la descripción sugieren que no necesariamente hay que limitarse a escuchar el audio sino que también podría ser útil ver como está representado visualmente.

Antes de abrirlo en un editor, empezamos con una inspección básica del archivo desde la terminal de Linux:

```bash
file 2senses_puzzle.wav
```

![Identificacion wav](./imágenes/Pasted%20image%2020261001170210.png)

El comando nos confirma que se trata de un archivo de audio **WAV / RIFF, PCM de 16 bits, mono y 44,1 kHz**.

A continuación, vamos a buscar cadenas de texto legibles dentro del archivo:

```bash
strings 2senses_puzzle.wav | tail -50
```

![Strings](./imágenes/Pasted%20image%2020261001170104.png)

Entre las cadenas encontradas aparece un fragmento que nos interesa por su formato muy similar al de una flag típica:

```text
CSSCTF{WHOS_THIS_FLUFFMASTER_MR...
```

Pero. como podemos ver, el contenido está **incompleto**. Esto nos aporta el dato de que una parte de la respuesta se encuentra almacenada como texto y que vamos a necesitar otro método para recuperar el resto de la flag.

Para comprobar de dónde viene esa información, revisamos los metadatos con la herramienta **ExifTool**:

```bash
exiftool -a -u -g1 2senses_puzzle.wav
```

![Metadatos](./imágenes/Pasted%20image%2020261001170252.png)

*Cabe destacar que los parámetros utilizados nos permiten detectar etiquetas repetidas que podrían contener información oculta (-a). Además puede mostrar campos no reconocidos (-u), y por último, agrupamos los metadatos según su ubicación dentro de la estructura del archivo. Información tomada de https://exiftool.org/exiftool_pod.html*

Continuando con el análisis, ExifTool nos muestra que el fragmento de la flag se encuentra en el campo `Artist` y que el campo `Comment` tiene la llave de cierre:

```text
Artist  : CSSCTF{WHOS_THIS_FLUFFMASTER_MR...
Comment : }
```

Esto nos confirma que la respuesta esta distribuida en distintas partes del archivo y que aún tenemos que encontrar la parte final de la flag ya que podemos ver que el fragmento termina con "...".

Para poder descartar que los puntos suspensivos fueran un recorte visual de la herramienta que acabamos de utilizar (indicando que podemos expandir el texto), podemos realizar otra comprobación a nivel de bytes utilizando la herramienta **hexdump**:

```bash
hexdump -C 2senses_puzzle.wav | tail -50
```

![Hexdump](./imágenes/Pasted%20image%2020261001170316.png)

En las últimas líneas podemos encontrar la secuencia hexadecimal:

```text
4d 52 2e 2e 2e
 M  R  .  .  .
```

Como podemos ver, los tres puntos forman parte del contenido real del archivo y no son caracteres que `strings` o ExifTool ocultaron automáticamente. Nos sigue faltando encontrar el fragmento que completa la flag.

Dado que el reto trata de audio, procedemos a abrir el WAV en **Audacity** y lo vamos a examinar de forma visual.

En Audacity podemos activar la vista de **espectrograma**. Esta espectograma nos va a servir para poder ver cómo se distribuyen las frecuencias del sonido a lo largo del tiempo y nos va a servir para descubrir texto o figuras interesantes dado nuestro análisis.

Por lo tanto, cambiamos la pista a la vista de espectrograma:

![Audacity onda](./imágenes/Pasted%20image%2020261001160727.png)

A continuación podemos el resultado obtenido:

![Audacity espectrograma](./imágenes/Pasted%20image%2020261001160825.png)

Inicialmente, la visualización muestra zonas de color intensas que nos imposibilitan poder interpretar de forma clara las letras o símbolos que se encuentran de fondo. Por lo tanto, para aumentar la legibilidad, ajustamos la configuración del espectrograma  incrementando el tamaño de ventana, cambiamos la representación a escala de grises y modificamos los parámetros de ganancia y rango.

![Configuracion espectrograma](./imágenes/Pasted%20image%2020261001161609.png)

Con estos ajustes, el contenido del espectrograma se vuelve más claro y legible, permitiéndonos interpretrar la palabra oculta:

```text
Chinaski
```

![Mensaje espectrograma](./imágenes/Pasted%20image%2020261001161653.png)

Ya tenemos los tres componentes que necesitamos para reconstruir la flag:

```text
campo Artist  -> CSSCTF{WHOS_THIS_FLUFFMASTER_MR...
Espectrograma -> Chinaski
campo Comment -> }
```

Procedemos a reemplazar los puntos suspensivos por el fragmento que faltaba y a reconstruir la flag, obteniendo como resultado final:

```text
CSSCTF{WHOS_THIS_FLUFFMASTER_MR_Chinaski}
```

Ingresamos el valor de la flag reconstruida en la plataforma, quedando resuelta de forma correcta.

![Ingreso flag](./imágenes/Pasted%20image%2020261001160520.png)

![Flag aceptada](./imágenes/Pasted%20image%2020261001165529.png)
