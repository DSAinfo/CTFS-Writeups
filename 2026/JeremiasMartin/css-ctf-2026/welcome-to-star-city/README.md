# Welcome to Star City

**CTF:** [CSS CTF 2026: Return of Nexus](https://ctftime.org/event/3434)  
**Categoría:** Web  
**Dificultad:** Fácil  
**Autor:** Michael Dalton  
**Fecha de resolución:** 30/09/2026  
**Reto:** Welcome to Star City

![Portada evento](./imágenes/Pasted%20image%2020261001152746.png)

![Enunciado](./imágenes/Pasted%20image%2020261001152907.png)

El enunciado nos introduce en la temática del reto a resolver, haciendo referencia a "Star City" y plantea si existe algo más de lo que podemos ver a simple vista. 
Esto nos da una primera pista, nos va a convenir revisar el contenido de la página más allá de su estética o apariencia visual.

Al ingresar a la página nos encontramos con una interfaz bastante sencilla, sólamente contamos con un cartel RGB en movimiento:

![Sitio inicial](./imágenes/Pasted%20image%2020261001152950.png)

Dado que no hay ningún formulario, botón u otra funcionalidad que nos permita interactuar, el siguiente paso es inspeccionar el código de la página mediante las herramientas de desarrollador (`F12`).

![Html](./imágenes/Pasted%20image%2020261001153043.png)

Como podemos observar, el HTML tiene una estructura simple y sólo cuenta con una referencia a la hoja de estilos llamado `style.css`. No encontramos información útil directamente en el HTML, así que procedemos a inspeccionar el CSS:

![Css inicial](./imágenes/Pasted%20image%2020261001153149.png)

Al revisar el código, observamos distintas reglas relacionadas con el fondo, la tipografía, el cartel y las animaciones.   
Al final del archivo aparece un comentario con una cadena que no se corresponde con ninguna propiedad CSS:

![Comentario css](./imágenes/Pasted%20image%2020261001153256.png)

```text
Q1NTQ1RGJTdCd2VfQlUxTFRfdGhpc19jaXR5X2Zyb21fcjBja19hbmRfUjAxMSU3RA
```

La cadena usa caracteres compatibles con **Base64**, por lo que vamos a probar decodificarla utilizando la herramienta CyberChef:

![Base64](./imágenes/Pasted%20image%2020261001153539.png)

Como podemos observar, el resultado empieza con `CSSCTF`, pero además posee fragmentos como `%7B` y `%7D`, que representan las llaves de apertura y cierre codificados en URL (porcentual). 
Dado que la flag todavía no es totalmente legible, agregamos una segunda operación o receta, **URL Decode**, después de **From Base64**.

![Url decode](./imágenes/Pasted%20image%2020261001153616.png)

De esta forma la secuencia de pasos utilizados para recuperar el texto fue:

```text
Comentario CSS -> From Base64 -> URL Decode -> Flag
```

La flag obtenida es:

```text
CSSCTF{we_BU1LT_this_city_from_r0ck_and_R011}
```

Finalmente, la ingresamos en la plataforma del reto, quedando resuelto de forma correcta.

![Ingreso flag](./imágenes/Pasted%20image%2020261001153659.png)

![Flag aceptada](./imágenes/Pasted%20image%2020261001153725.png)

