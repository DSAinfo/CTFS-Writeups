## NullOrigin CTF Qualifiers

# The Forbidden Six

**CTF:** NullOrigin CTF Qualifiers  
**Categoría:** Web  
**Dificultad:** Easy  
**Autor:** CYBXMONK  
**Fecha de resolución:** 18/09/2026  
**Reto:** [The Forbidden Six](https://nullorigin.cyberhx.com/)  
**Evento:** [NullOrigin CTF Qualifiers - CTFtime](https://ctftime.org/event/3346)


![Portada del evento](./imágenes/Imagen%20pegada.png)

![Portada del reto The Forbidden Six](./imágenes/Imagen%20pegada%20(2).png)

Al acceder a la instancia del reto, podemos observar la página correspondiente al tablero de Ludo de la aplicación:

![Estado inicial del tablero de Ludo](./imágenes/Imagen%20pegada%20(3).png)

Como información, el juego nos informa que la ficha `Token #4` se encuentra a seis posiciones del final y el dado tiene un valor fijo de `6`.

Por lo tanto, aparentemente alcanza con mover esa ficha para finalizar el juego.
Sin embargo, la propia interfaz nos muestra `Winning moves are disabled.`

Por lo tanto, como primera prueba clickeamos en el botón **Move Token #4**.

![Intento de realizar el movimiento ganador](./imágenes/Imagen%20pegada%20(4).png)

El intento queda registrado en el `SYSTEM LOG` que podemos ver a la derecha, pero la aplicación responde:

```text
SYSTEM: Winning moves are disabled.
```

Esto nos indica que existe algún impedimento encargado de bloquear el movimiento ganador/final.

Entonces para poder determinar dónde se encuentra implementada esta restricción, vamos a inspeccionar el código de la app utilizando la herramienta de desarrollador del browser (`F12`).

En el HTML aparece un comentario indicando que una vulnerabilidad relacionada con `/api/move` habría sido corregida y además menciona una posible "race condition" en `/api/reset`.

![Comentarios encontrados en el código HTML](./imágenes/Imagen%20pegada%20(5).png)

Dado que sólo de trata de información incluida en el frontend, seguimos revisando el JavaScript para chequear cómo funciona realmente la app.

En `app.js` encontramos comentarios similares indicando que el endpoint `/api/move` supuestamente realiza nuevamente la validación del movimiento en el servidor.

![Comentarios de seguridad encontrados en app.js](./imágenes/Imagen%20pegada%20(6).png)

El archivo además nos muestra distintas flags falsas o "señuelos":

![Flags falsas encontradas en app.js](./imágenes/Imagen%20pegada%20(7).png)

Por lo tanto, estas pistas que nos provee el código NO se consideran información relevante para poder entender el comportamiento real del backend.


Si seguimos analizando el código podemos ver el estado inicial definido en `app.js`:


![Estado inicial del juego definido en app.js](./imágenes/Imagen%20pegada%20(8).png)

Como podemos ver en la captura, las fichas/tokens `1`, `2` y `3` ya se encuentran finalizadas (finished=true), mientras que la ficha `4` está a seis posiciones antes del final.

Por otro lado, la función `simulateMove()` lo que hace es calcular el resultado del movimiento:

![Función simulateMove](./imágenes/Imagen%20pegada%20(9).png)

Como el dado tiene un valor de `6`, mover `Token #4` hace que la ficha llegue al valor `PATH_LENGTH`, esto hace que la simulación determine que el jugador rojo gana el juego.

Este resultado se va a utilizar luego por otra función que se llama `validateMove()`.

![Función validateMove](./imágenes/Imagen%20pegada%20(10).png)

Dentro de esta función vamos a encontrar la siguiente restricción:

```javascript
if (simulated.winner) {
  showSystemNotice("Winning moves are disabled.");
  return false;
}
```

Es decir, cuando el browser detecta que el movimiento produciría una win, cancela la operación antes de enviarla al server.

Esto lo podemos ver también en la función `makeMove()`:

![Función makeMove](./imágenes/Imagen%20pegada%20(11).png)

La llamada que manda el movimiento es:

```javascript
const data = await sendMove(move);
```

sólo se ejecuta cuando `validateMove()` le deja continuar.

Es por esto que el botón de la interfaz nunca llega a enviar el movimiento ganador al backend.


Entonces, si seguimos viendo el código, podemos ver que en la función `sendMove()` encontramos el endpoint que usa la app:

![Función sendMove y endpoint api move](./imágenes/Imagen%20pegada%20(12).png)

La función realiza un requerimiento `POST /api/move` enviando el movimiento mediante JSON.

En este caso, el movimiento correspondiente a la ficha número 4 es:

```json
{
  "token": 4,
  "dice": 6
}
```

Como la restricción que vemos pertenece al frontend, podemos evitarla o "saltearla" realizando directamente la petición al endpoint desde la consola del navegador (`F12`):

```javascript
fetch("/api/move", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    token: 4,
    dice: 6
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

![Petición manual al endpoint api move](./imágenes/Imagen%20pegada%20(13).png)

El servidor lo que hace es procesar el movimiento y nos devuelve una respuesta exitosa junto a la flag del reto:

```json
{
  "ok": true,
  "winner": "red",
  "flag": "NullOrigin{tH3_c1ient_siD3_spe4ks_th3_TrUth}"
}
```

A modo de resumen pudimos demostrar que el bloqueo de realizar movimientos ganadores que mencioné al principio se encontraba implementada SÓLAMENTE en el cliente y podía evitarse o saltearse mandando directamente la solicitud HTTP.

Por último, ingresamos la flag obtenida en la plataforma, quedando el reto resuelto de forma correcta.

![Ingreso de la flag obtenida en The Forbidden Six](./imágenes/Imagen%20pegada%20(14).png)

![Reto The Forbidden Six resuelto](./imágenes/Imagen%20pegada%20(15).png)