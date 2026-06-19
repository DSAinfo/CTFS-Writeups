# X-Ray Vision
## Categoría: Web

### Tenemos el siguiente enunciado:
<img width="507" height="631" alt="enun" src="https://github.com/user-attachments/assets/e5e14a94-d2c7-49f5-8763-59dabaf50a7e" />

En el enunciado nos da la pista que hay una credencial olvidada en alguna parte de la página web, y que no está en texto plano.

La página web nos muestra:
<img width="1365" height="728" alt="web" src="https://github.com/user-attachments/assets/70b7c597-0912-443d-a371-354a842d56ba" />

Lo único interactivo es el boton de “query api”, si hacemos click obtenemos:
<img width="1365" height="725" alt="hint0" src="https://github.com/user-attachments/assets/1a1bf836-ffaa-4736-b35a-5fb4decfcfc0" />

Nos aparece el mensaje: “status: unathorized missing token”. Con esta pista lo que hacemos es inspeccionar la pagina con burp suite y encontramos:
<img width="1365" height="726" alt="x-secret-token" src="https://github.com/user-attachments/assets/33e19573-0087-46bc-bbac-b5d806b2ef1b" />
<img width="812" height="268" alt="token" src="https://github.com/user-attachments/assets/5d61dd7b-1473-4a3b-81f2-a57f267a337a" />

Con esta nueva información, interceptamos la petición que se hace al hacer click en “query api”, y agregamos la cabecera “x-secret-token” con el valor que aparece en data-t.
<img width="1365" height="726" alt="intercept1" src="https://github.com/user-attachments/assets/b1b06664-35ec-4061-a450-db2c6644002b" />

Al hacer forward, obtenemos ahora 
<img width="821" height="108" alt="hint1" src="https://github.com/user-attachments/assets/c1a7f780-b41c-4d57-9741-93674da9d01f" />

Si tomamos el valor del token anterior y probamos decodificarlo con rot13, obtenemos:
<img width="1365" height="727" alt="rot13web" src="https://github.com/user-attachments/assets/b8fbd19b-0dbc-4c2f-b87b-05dc9969c3e1" />


Se obtiene : “d3v3l0p3r_t00l5”, esta no es la flag, asi que probamos interceptar de nuevo la peticion a /api , agregando de nuevo la cabecera de “x-secret-token” con el nuevo valor:
<img width="1365" height="650" alt="intecept2" src="https://github.com/user-attachments/assets/1ba14a10-b4bd-40d9-bd0a-7b7334378062" />


Finalmente obtenemos:
<img width="748" height="184" alt="zoomflag" src="https://github.com/user-attachments/assets/6b6d2fa9-1ce3-4ec1-80af-a02da72212c5" />


Flag:  jctf{r0t_y0ur_w4y_t0_4cc3ss}

