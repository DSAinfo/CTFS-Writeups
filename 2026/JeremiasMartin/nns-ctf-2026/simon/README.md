## NNS CTF 2026

# Simon

**CTF:** NNS CTF 2026  
**Categoría:** Web  
**Dificultad:** Beginner  
**Autor:** pipreth  
**Fecha de resolución:** 06/09/2026  
**Reto:** [Simon](https://nnsc.tf/)  
**Evento:** [NNS CTF 2026 - CTFtime](https://ctftime.org/event/3097)

![Portada del evento](./imágenes/Imagen%20pegada.png)

![Portada del reto Simon](./imágenes/Imagen%20pegada%20(2).png)


Al iniciar la instancia accedemos a una página correspondiente al vuelo **NNS4043**, donde se muestra un gráfico con los distintos asientos disponibles.

![Mapa de selección de asientos del vuelo NNS4043](./imágenes/Imagen%20pegada%20(3).png)

Podemos distinguir diferentes tipos de asientos según su color y disponibilidad.

Los asientos **azules**, ubicados en las filas inferiores, corresponden a los asientos disponibles para usuarios normales.

En cambio, algunos asientos aparecen en **amarillo**, indicando que pertenecen a **NNS Air Plus**, el servicio premium de la aerolínea.

La propia interfaz nos muestra el mensaje:

> Only NNS Air Plus infront

Esto nos indica que los mejores asientos se encuentran reservados exclusivamente para usuarios que poseen la categoría **NNS Air Plus**.

Para poder entender cómo se implementa esta restricción inspeccionamos el código HTML de la página mediante las herramientas de desarrollador del browser (`F12`).

![Inspección de los asientos premium en el código HTML](./imágenes/Imagen%20pegada%20(4).png)

Podemos observar que los asientos premium tienen una estructura similar a la siguiente:

```html
<button
  type="button"
  class="seat seat--premium"
  data-seat="3B"
  data-status="premium"
  aria-label="Seat 3B, premium"
>
  <span class="seat-back" aria-hidden="true"></span>
  <span class="seat-cushion" aria-hidden="true"></span>
</button>
```

En particular, el asiento `3B` tiene el "campo-valor":

```html
data-status="premium"
```

Por otro lado, los asientos disponibles para usuarios normales tienen una estructura similar a la siguiente:

```html
<button
  type="button"
  class="seat seat--available"
  data-seat="8A"
  data-status="available"
  aria-label="Seat 8A, available"
>
  <span class="seat-back" aria-hidden="true"></span>
  <span class="seat-cushion" aria-hidden="true"></span>
</button>
```

La diferencia más importante se encuentra en el campo:

```html
data-status="available"
```

frente a:

```html
data-status="premium"
```

Esto nos ayuda a identificar que la aplicación utiliza el valor almacenado en `data-status` para determinar si un asiento puede ser seleccionado o no desde la interfaz.

Dado que el campo `data-status` forma parte del HTML cargado en nuestro browser, podemos modificarlo de forma local.

Seleccionamos uno de los asientos premium, concretamente el asiento `3B` y modificamos:

```html
data-status="premium"
```

por:

```html
data-status="available"
```

De esta manera, el elemento queda con una estructura similar a:

```html
<button
  type="button"
  class="seat seat--premium seat--selected"
  data-seat="3B"
  data-status="available"
  aria-label="Seat 3B, premium"
  aria-pressed="true"
>
  <span class="seat-back" aria-hidden="true"></span>
  <span class="seat-cushion" aria-hidden="true"></span>
</button>
```

El asiento sigue manteniendo la clase visual `seat--premium` pero su estado pasa a ser `data-status="available"`.

La aplicación permite entonces seleccionar el asiento premium como si se tratara de un asiento disponible para un usuario normal.

![Asiento premium 3B seleccionado después de modificar data-status](./imágenes/Imagen%20pegada%20(5).png)

En la interfaz podemos comprobar que el asiento `3B`, inicialmente amarillo, aparece ahora seleccionado en color verde.

Además, en la parte inferior se muestra la leyenda:

```text
Selected seat 3B
```

y el botón **Save** queda habilitado.


Una vez seleccionado el asiento premium `3B`, confirmamos la elección mediante el botón **Save**.

La aplicación acepta nuestra elección y posteriormente muestra en pantalla:

```text
Your NNS Air Plus flag benefit
```

![Flag mostrada al reservar el asiento premium](./imágenes/Imagen%20pegada%20(6).png)

El mensaje indica que, como beneficio de NNS Air Plus, se proporciona una flag exclusiva.

La flag obtenida es:

```text
NNS{w3_W1sH_You_4_p13a54N7_F1i6H7_W17H_NNs_41r}
```

Finalmente, ingresamos la flag obtenida en la plataforma del CTF, quedando el reto resuelto de forma correcta.

![Ingreso de la flag obtenida en el reto Simon](./imágenes/Imagen%20pegada%20(7).png)

![Challenge solved del reto Simon](./imágenes/Imagen%20pegada%20(8).png)