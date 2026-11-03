## Writeup: Poisoned Well

**CTF:** Pointer Overflow CTF 2026
**Categoría:** Web
**Dificultad:** Fácil / Media (97 pts)

## Explotación y Verificación de la Vulnerabilidad
Con las premisas teóricas sobre la arquitectura del servidor claras, procedí a evaluar el comportamiento de la caché y la sesión.

Al realizar pruebas de reconocimiento mediante peticiones HTTP directas con curl, la aplicación devolvía un redireccionamiento 302 Found hacia /login o respuestas 401 Unauthorized. Esto confirmó que el proxy inverso exige una sesión activa asociada para procesar y almacenar las respuestas de la aplicación.

Utilizando la sesión autenticada en el navegador web con el token asignado, accedí inicialmente al endpoint /verify para comprobar el estado de la caché del servidor. El backend devolvió la siguiente respuesta en formato JSON:

```{"ok": false, "reason": "cache is cold — visit / first"}```

Este mensaje confirmó la mecánica planteada en las notas del desafío: para que la regla de almacenamiento en caché se active, el proxy inverso (Nginx/1.24.0) requiere que existan peticiones previas hacia la ruta raíz (/) que permitan generar y guardar la respuesta en memoria ("calentar" la caché).

Al navegar a la raíz (/) con la sesión autenticada activa, Nginx procesó la solicitud inicial hacia el backend. Dado que la clave de la caché (cache key) está configurada para tomar únicamente la ruta y la cookie de sesión (omitiendo encabezados de redirección como X-Forwarded-Host), el proxy guardó la respuesta generada por el backend en memoria de borde durante su tiempo de vida (TTL).

Posteriormente, al consultar nuevamente el endpoint /verify, el sistema leyó el recurso retenido en la caché, confirmó que el proxy reflejaba dinámicamente las cabeceras no incluidas en la cache key y entregó el estado exitoso junto con la bandera del desafío:
```{
  "cached_host": "poisoned-well.pointeroverflowctf.com/",
  "flag": "POCTF{82.1287.AYWTBG7XQIFIULAO.6UTLUEMDE642M2EQOIEZEIKI3X}",
  "message": "Cache has been poisoned. The next visitor to / would see your canonical URL instead of the legitimate one. That is the vulnerability — congratulations.",
  "nonce": "AYWTBG7XQIFIULAO",
  "ok": true
}
```
## Conclusiones del Hallazgo
La prueba de concepto confirmó una falla de diseño en la configuración del proxy inverso:

Unkeyed Inputs: El proxy inverso no incluye las cabeceras X-Forwarded-* dentro de la clave de almacenamiento (cache key).

Inyección en Backend: El servidor de aplicaciones utiliza de forma implícita la cabecera X-Forwarded-Host enviada por el cliente para construir la URL canónica del sitio.

Persistencia: Al coincidir la cache key de peticiones subsecuentes, cualquier usuario que solicite la ruta raíz (/) dentro del TTL de 60 segundos recibirá la respuesta manipulada envenenada previamente en la caché.