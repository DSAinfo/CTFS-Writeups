
# Writeup: Solución al challenge SecurityValley - Cookie Api

El reto consiste en encontrar una forma de crear una cookie para el endpoint /api/v1/store que fuera aceptada por el servidor.

![IMAGEN]

## Paso 1: Inspección inicial
Al acceder al enlace del reto, podemos ver que existen dos endpoints: /api/v1/init y /api/v1/store. Se deduce que el endpoint /api/v1/init es el responsable de crear la cookie.

![IMAGEN]

Para verificar esto, realizamos una solicitud CURL al endpoint /api/v1/init y confirmamos que se crea una cookie con nombre "session_token" y valor en base64. Además, podemos observar que el tiempo de expiración es de solo 1 milisegundo, lo que significa que la cookie es válida por muy poco tiempo.

## Paso 2: Scripting con Python
Dado que la cookie creada manualmente tiene un tiempo de expiración muy corto, podemos intentar resolver el reto creando un script en Python que realice el proceso automáticamente.

Primero, hacemos una solicitud a /api/v1/init para obtener la cookie y guardamos su valor.

Luego, intentamos crear una nueva cookie con el mismo nombre y valor que la cookie obtenida, y la enviamos en una solicitud a /api/v1/store. Sin embargo, obtenemos una respuesta con un código de estado 401 no autorizado.

![IMAGEN]
![IMAGEN]

## Paso 3: Manipulando la cookie
Decidimos decodificar el valor de la cookie obtenida en base64 y encontramos que tiene el formato "role=&id=". Observamos que el valor del campo "role" está establecido en "user".

![IMAGEN]
![IMAGEN]

Intuitivamente, sospechamos que el servidor verifica la identidad del usuario a través del valor "role". Por lo tanto, intentamos cambiar el valor "user" a "admin" y volvemos a codificar la cadena en base64.

![IMAGEN]
![IMAGEN]

## Paso 4: Enviar la nueva cookie
Finalmente, enviamos la nueva cookie con el nombre "session_token" y el valor codificado en base64 que contiene el nuevo valor "admin" en el campo "role" en una solicitud a /api/v1/store.

Al hacer esto, obtenemos una respuesta con un código de estado 200 y el flag del reto "SecVal{I_LIKE_C00K1S}".

![IMAGEN]
![IMAGEN]
![IMAGEN]
![IMAGEN]









