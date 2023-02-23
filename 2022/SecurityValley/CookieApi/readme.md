
# Writeup: Solución al challenge SecurityValley - Cookie Api

El reto consiste en encontrar una forma de crear una cookie para el endpoint /api/v1/store que fuera aceptada por el servidor.
![imagen1](https://user-images.githubusercontent.com/37942177/220953036-ed41cbfe-5e44-4720-b824-6e0ddfd8079d.png)


## Paso 1: Inspección inicial
Al acceder al enlace del reto, podemos ver que existen dos endpoints: /api/v1/init y /api/v1/store. Se deduce que el endpoint /api/v1/init es el responsable de crear la cookie.
![imagen2](https://user-images.githubusercontent.com/37942177/220953338-6fc3e0ce-e321-4d24-bedb-1899bbd5c5b5.png)

Para verificar esto, realizamos una solicitud CURL al endpoint /api/v1/init y confirmamos que se crea una cookie con nombre "session_token" y valor en base64. Además, podemos observar que el tiempo de expiración es de solo 1 milisegundo, lo que significa que la cookie es válida por muy poco tiempo.

## Paso 2: Scripting con Python
Dado que la cookie creada manualmente tiene un tiempo de expiración muy corto, podemos intentar resolver el reto creando un script en Python que realice el proceso automáticamente.

Primero, hacemos una solicitud a /api/v1/init para obtener la cookie y guardamos su valor.

Luego, intentamos crear una nueva cookie con el mismo nombre y valor que la cookie obtenida, y la enviamos en una solicitud a /api/v1/store. Sin embargo, obtenemos una respuesta con un código de estado 401 no autorizado.
![imagen3](https://user-images.githubusercontent.com/37942177/220953685-0e977632-c404-4b36-afda-43581f9fd94d.png)
![imagen4](https://user-images.githubusercontent.com/37942177/220953854-4f7f7c65-b191-4af9-8818-11f942259d31.png)

## Paso 3: Manipulando la cookie
Decidimos decodificar el valor de la cookie obtenida en base64 y encontramos que tiene el formato "role=&id=". Observamos que el valor del campo "role" está establecido en "user".
![imagen5](https://user-images.githubusercontent.com/37942177/220954251-95214f1e-2487-45aa-bb9a-363ed3c1414e.png)
![imagen6](https://user-images.githubusercontent.com/37942177/220954348-f27c4584-766f-4ba7-b1f1-22894e275138.png)

Intuitivamente, sospechamos que el servidor verifica la identidad del usuario a través del valor "role". Por lo tanto, intentamos cambiar el valor "user" a "admin" y volvemos a codificar la cadena en base64.
![imagen7](https://user-images.githubusercontent.com/37942177/220954697-a4929b07-bcd2-4bce-b730-35110f5c000e.png)
![imagen8](https://user-images.githubusercontent.com/37942177/220954760-071f93aa-83e0-4b93-9a7b-a02aeafc799e.png)

## Paso 4: Enviar la nueva cookie
Finalmente, enviamos la nueva cookie con el nombre "session_token" y el valor codificado en base64 que contiene el nuevo valor "admin" en el campo "role" en una solicitud a /api/v1/store.

Al hacer esto, obtenemos una respuesta con un código de estado 200 y el flag del reto "SecVal{I_LIKE_C00K1S}".
![imagen9](https://user-images.githubusercontent.com/37942177/220958688-78bc2480-a9d3-4e8a-9109-aebc85ccd9fe.png)
![imagen10](https://user-images.githubusercontent.com/37942177/220958730-74d65695-1108-4e1b-b776-333ba0e1f866.png)
![imagen11](https://user-images.githubusercontent.com/37942177/220958794-cf261c32-725b-4b1f-92ee-bc0d514d76f5.png)










