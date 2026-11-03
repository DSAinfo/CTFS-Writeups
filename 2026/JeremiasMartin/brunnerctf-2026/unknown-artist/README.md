# Unknown Artist

**CTF:** BrunnerCTF 2026  
**Categoría:** OSINT  
**Dificultad:** Fácil  
**Autor:** Ha1fdan  
**Fecha de resolución:** 22/08/2026  
**Reto:** [Unknown Artist](https://global.brunnerctf.dk/challenges#Unknown%20Artist-82)

![BrunnerCTF 2026](./imágenes/Imagen%20pegada%20(11).png)


![Información del reto](./imágenes/Imagen%20pegada%20(1).png)

El reto inicialmente nos provee un archivo ZIP que contiene una canción en formato MP3 llamada `Brunnerne Inc.mp3`.

Al reproducirla podemos ver que la propia letra nos brinda varias pistas sobre cómo continuar con el análisis y resolución. 
Entre las frases que más llaman la atención aparecen referencias como:

```text
Check the metadata, trace the sound wave clear
Look inside the properties, read between the lines
EXIF tags and UUIDs give away the signs
Search the profile... Match the ID...
```

También se menciona que existen varias canciones publicadas.
Todo esto apunta a que el archivo contiene información útil más allá del audio.

Por lo tanto, el siguiente paso es revisar los metadatos del audio. 
Para hacerlo utilizamos la herramienta **ExifTool**:

```bash
exiftool "Brunnerne Inc.mp3"
```

![Metadatos del archivo](./imágenes/Imagen%20pegada%20(2.2).png)
![Metadatos del archivo Parte 2](./imágenes/Imagen%20pegada%20(2.3).png)

Entre las distintas etiquetas ID3 encontramos el título, la letra y otros datos relacionados con el archivo. Sin embargo, el campo más interesante fue `Source URL`:

```text
Title       : Brunnerne Inc
Source URL  : https://suno.com/song/b408fe76-c81f-4a96-b10e-b9df4e5d4ec2
```

La URL apunta directamente a una publicación de **Suno** (plataforma de música), por lo que coincide con las pistas que nos dió la canción sobre revisar los metadatos, buscar el perfil y seguir los id's encontrados.

Al ingresar al enlace llegamos a la publicación original de `Brunnerne Inc`.

![Publicación original en Suno](./imágenes/Imagen%20pegada%20(3).png)

En la descripción de la canción aparece una cadena que a simple vista no tiene demasiado significado:

```text
YnJ1bm5lcntmcg==
```

En base a su formato podemos deducir que esta codificada en **Base64**. En lugar de tratarla como un mensaje completo, la tomamos como una posible parte de la flag.

El siguiente paso es acceder al perfil del autor de la canción. Ahí encontramos varias publicaciones del mismo usuario.

![Perfil del autor](./imágenes/Imagen%20pegada%20(4).png)

Revisamos las demás canciones buscando el mismo patrón y encontramos cadenas nuevas en sus descripciones.

![Canción del perfil](./imágenes/Imagen%20pegada%20(5).png)

![Canción del perfil](./imágenes/Imagen%20pegada%20(6).png)

![Canción del perfil](./imágenes/Imagen%20pegada%20(7).png)

Las cuatro cadenas obtenidas fueron:

```text
YnJ1bm5lcntmcg==
MG1fbTM3NGQ0Nw==
NF83MF81M2NyMw==
N181MG45fQ==
```

Como todas tenían el formato esperado de Base64, las reunimos y utilizamos la herramienta CyberChef para decodificarlas.

![Decodificación Base64](./imágenes/Imagen%20pegada%20(8).png)

Al decodificar los fragmentos y unirlos en el orden correspondiente obtuvimos:

```text
brunner{fr0m_m374d474_70_53cr37_50n9}
```

Finalmente ingresamos el valor obtenido en la plataforma de BrunnerCTF y el reto queda resuelto de forma correcta.

![Flag aceptada](./imágenes/Imagen%20pegada%20(9).png)
![Flag aceptada](./imágenes/Imagen%20pegada%20(10).png)