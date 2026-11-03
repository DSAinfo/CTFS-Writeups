# Colour Shift

**CTF:** [CSS CTF 2026: Return of Nexus](https://ctftime.org/event/3434)  
**Categoría:** Esteganografía  
**Dificultad:** Principiante   
**Fecha de resolución:** 30/09/2026  
**Reto:** Colour Shift

![Portada evento](./imágenes/Pasted%20image%2020261001152746.png)

![Enunciado](./imágenes/Pasted%20image%2020261001153804.png)

El enunciado del reto hace referencia a Isaac Newton y a la separación de la luz en sus distintos colores. 
Además, el reto nos provee una imagen en formato BMP.

A partir de esta pista inicial, podemos pensar que el reto está relacionado con los colores de la imagen y que probablemente tengamos que manipularlos de alguna forma para encontrar información oculta.

Descargamos el archivo y lo abrimos en la herramienta GIMP: 

![Imagen gimp](./imágenes/Pasted%20image%2020261001153932.png)

A primera vista, podemos ver que la imagen corresponde a la portada del álbum The Dark Side of the Moon, de Pink Floyd, donde aparece una figura que recibe luz blanca y lo separa en los colores del arcoíris.

Como no encontramos ninguna flag, teniendo en cuenta la idea/concepto de la imagen, procedemos a realizar la separación de los canales de color utilizando las opciones de GIMP.

Desde el menú de GIMP accedemos a **Colores -> Componentes -> Descomponer**.

![Menu descomponer](./imágenes/Pasted%20image%2020261001154035.png)

En la ventana de configuración seleccionamos el modelo de color **RGB** y activamos la opción **Descomponer en capas**.

![Descomposicion RGB](./imágenes/Pasted%20image%2020261010211333.png)

El modelo RGB representa los colores mediante sus tres capas:

- R (Red/rojo): información correspondiente al canal rojo.

- G (Green/verde): información correspondiente al canal verde.

- B (Blue/azul): información correspondiente al canal azul.

Al descomponer la imagen, GIMP genera tres capas en escala de grises, una por cada canal. 
Esto nos va a permitir analizar la información de cada color por separado.


Después de aplicar la operación, GIMP genera las capas correspondientes a los tres canales:

![Capas RGB](./imágenes/Pasted%20image%2020261010211354.png)

Para hacer que las letras fueran más visibles, seleccionamos la capa correspondiente al canal rojo y accedemos a **Colores -> Niveles**.

![Niveles](./imágenes/Pasted%20image%2020261010210132.png)

*Esta opción nos va a permitir modificar cómo se distribuyen los distintos tonos (oscuros, medios y claros) de la imagen -
Información tomada de https://docs.gimp.org/3.0/en/gimp-tool-levels.html*

Para nuestro caso, el texto está mezclado con un fondo muy oscuro, por lo que vamos a necesitar aclarar la imagen para poder distinguirlo.

Por lo tanto vamos a modificar el apartado de "Niveles de entrada" (gráfico de barras), seteando el valor de gamma (para poder aclarar la mayor parte de la imagen) hasta 10 sin tocar el resto de parámetros.

Obtendremos como resultado:


![Imagen obtenida](./imágenes/Pasted%20image%2020261010210143.png)

El resultado que obtenemos es la visualización de un texto que corresponde con el formato típico de una flag.

Si bien la flag ya se puede leer, todavía aparece ruido en la imagen, producto de aclarar tanto el canal rojo.

Si queremos visualizar el texto de forma más clara, podemos, como último paso, intentar reducir los puntos o manchas negras.
Para esto vamos a usar el filtro "Desenfoque de mediana" ubicado en las opciones **Filtros -> Difuminar -> Desenfoque de Mediana**.

*Información tomada de https://docs.gimp.org/3.2/en/gimp-filter-median-blur.html*.

![Desenfoque Mediana](./imágenes/Pasted%20image%2020261010210842.png)

Para poder disminuir la cantidad de manchas o puntos aislado, este filtro lo que va a hacer es analizar los píxeles y cambiar sus valores utilizando un criterio estadístico.

Los valores que modificamos de forma manual fueron "Percentil" y "Radio" buscando un equilibro que nos permita mejorar la calidad de la imagen.

![Imagen Mejorada](./imágenes/Pasted%20image%2020261010210853.png)

Finalmente, el mensaje oculto nos permite identificar la siguiente flag:

```text
CSSCTF{SHINE_ON}
```

La ingresamos en la plataforma del reto quedando resuelto correctamente.

![Ingreso flag](./imágenes/Pasted%20image%2020261001154951.png)

![Flag aceptada](./imágenes/Pasted%20image%2020261001155007.png)
