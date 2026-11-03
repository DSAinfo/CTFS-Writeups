## NNS CTF 2026

# NNS Travel

**CTF:** NNS CTF 2026  
**Categoría:** Web  
**Dificultad:** Beginner  
**Autor:** pipreth  
**Fecha de resolución:** 06/09/2026  
**Reto:** [NNS Travel](https://nnsc.tf/)  
**Evento:** [NNS CTF 2026 - CTFtime](https://ctftime.org/event/3097)

![Portada del evento](./imágenes/Imagen%20pegada.png)

![Portada del Reto](./imágenes/Imagen%20pegada%20(2).png)

El reto nos provee el archivo `web_nns-travel.tar.gz`, que contiene el código fuente de la aplicación.

Al iniciar la instancia y acceder a la aplicación web nos encontramos con la página **NNS Air Travel Agency**.

La aplicación nos muestra que estamos autenticados en representación de **ACME Inc.** y nos permite agregar manualmente un viaje introduciendo una referencia de reserva mediante el campo **Booking Reference**.

![Página principal de NNS Air Travel Agency](./imágenes/Imagen%20pegada%20(3).png)

Como primera prueba, ingresamos una referencia inexistente:

```text
AAAAAA
```

La aplicación responde:

```text
Ticket not found.
```

![Mensaje Ticket not found al ingresar una referencia inexistente](./imágenes/Imagen%20pegada%20(4).png)

Esto indica que la referencia que ingresamos es utilizada para buscar algún recurso asociado a un ticket. Mismo ocurre si ingresamos inputs que nos permiten forzar el error de la página, como el caracter (') para obtener más información útil.

Respecto al archivo proporcionado por el reto, contiene la estructura completa del proyecto. Entre los elementos principales encontramos:

```text
bun.lock
Dockerfile
package.json
src/
tickets/
tsconfig.json
.gitignore
```

![Estructura de archivos del proyecto NNS Travel](./imágenes/Imagen%20pegada%20(5).png)

Dentro del directorio `src/` encontramos:

```text
index.ts
static/
travel.html
```

![Contenido del directorio src](./imágenes/Imagen%20pegada%20(6).png)

Por otro lado, dentro del directorio `tickets/` existe el archivo `HACKER.json`.

Su contenido es:


![Contenido del archivo HACKER.json](./imágenes/Imagen%20pegada%20(7).png)

El campo `solution` nos brinda una pista importante:

```text
No guessing is required for this challenge :P
```

Por lo tanto, el objetivo no consiste en realizar fuerza bruta sobre posibles referencias de reserva, sino en analizar cómo la aplicación procesa los archivos correspondientes a los tickets.


Al analizar el backend, precisamente `src/index.ts`, encontramos la implementación del servidor:

![Código del backend en index.ts](./imágenes/Imagen%20pegada%20(8).png)

El endpoint que nos resulta interesante es:

```text
POST /get-file
```

Este endpoint obtiene el parámetro `pnr` directamente desde la URL:

```typescript
const ticket = url.searchParams.get('pnr');
```

Posteriormente, utiliza ese valor para construir la ruta del archivo:

```typescript
const f = Bun.file('./tickets/' + ticket);
```

Acá está el problema y es que el contenido de `pnr` se concatena directamente con:

```text
./tickets/
```

sin realizar ninguna validación o saneamiento de la path.

Por ejemplo, si se enviara:

```text
HACKER.json
```

el servidor intentaría acceder a:

```text
./tickets/HACKER.json
```

Por lo tanto, al no existir controles que impidan que utilicemos secuencias como `../`, es posible intentar salir del directorio `tickets`.

Esta vulnerabilidad vista en la materia se conoce como **Path Traversal**.  
Explotando esta vulnerabilidad podemos acceder de forma arbitraria al sistema de archivos del servidor el cual aloja la aplicación web.


Antes de explotar la vulnerabilidad analizamos también el formulario HTML.

El campo correspondiente a la referencia tiene las siguientes características:

```html
<input
  id="ticket-id"
  type="text"
  name="ticket-id"
  placeholder="ABCDEF"
  maxlength="6"
  minlength="6"
>
```

![Restricciones del campo Booking Reference en el HTML](./imágenes/Imagen%20pegada%20(9).png)

Por lo tanto, desde la interfaz el identificador debe tener exactamente seis caracteres.

Debemos tener en cuenta que estas restricciones pertenecen únicamente al frontend, por lo tanto, no representan restricciones aplicadas por el servidor.

Esto queda más claro si analizamos el JavaScript utilizado por la página:


![JavaScript encargado de procesar las referencias de reserva](./imágenes/Imagen%20pegada%20(10).png)

El frontend lleva a cabo tres transformaciones importantes sobre el input que ingresamos:

1. Limita la longitud de la referencia a seis caracteres mediante:

```html
maxlength="6"
minlength="6"
```

2. Convierte automáticamente el valor ingresado a mayúsculas:

```javascript
.toUpperCase()
```

3. Agrega automáticamente la extensión `.json`:

```javascript
fetch(`get-file?pnr=${ticketId}.json`, ...)
```

Por ejemplo, si introducimos:

```text
HACKER
```

la petición/requerimiento generado se convierte en:

```text
/get-file?pnr=HACKER.json
```

Por lo tanto, estas restricciones no nos permiten introducir desde el formulario una ruta arbitraria como por ejemplo:

```text
../../../../flag.txt
```
Ya que eventualmente su extensión se va a modificar.   
Sin embargo, como mencioné anteriormente, se trata únicamente de controles implementados en el browser.

El endpoint del backend NO chequea ninguna de estas condiciones.

Continuando con en análisis, sabemos por el propio enunciado del reto, que la flag se encuentra en:

```text
/flag.txt
```

Por otro lado, el servidor intenta acceder a los archivos mediante:

```typescript
Bun.file('./tickets/' + ticket)
```

Entonces podemos utilizar secuencias `../` para retroceder en la estructura de directorios hasta alcanzar la raíz del sistema de archivos.

En lugar de hacer uso el formulario, que nos restringe la posibilidad de acceder a archivos que no sean `.json`, realizamos directamente un requerimiento HTTP desde la consola del navegador:

```javascript
fetch('/get-file?pnr=../../../../flag.txt', {
  method: 'POST'
})
.then(r => r.text())
.then(console.log);
```

De esta manera evitamos o "salteamos" las restricciones implementadas por `travel.html`.

La ruta construida internamente por el servidor pasa a ser:

```text
./tickets/../../../../flag.txt
```

Estas secuencias `../` nos van a permitir retroceder por los directorios del servidor hasta llegar a `/`, haciendo que finalmente el servidor acceda al archivo:

```text
/flag.txt
```

El backend no detecta ni bloquea el salto de directorios y devuelve directamente el contenido del archivo que solicitamos.

![Explotación del Path Traversal desde la consola del navegador](./imágenes/Imagen%20pegada%20(11).png)

La respuesta obtenida contiene la flag:

```text
NNS{wHoop5_yoU_found_a_P47H_7Ravers41_iN_My_coDe}
```

Finalmente, ingresamos la flag obtenida en la plataforma del CTF, quedando el reto resuelto de forma correcta.

![Ingreso de la flag obtenida en NNS Travel](./imágenes/Imagen%20pegada%20(12).png)

![Challenge solved de NNS Travel](./imágenes/Imagen%20pegada%20(13).png)