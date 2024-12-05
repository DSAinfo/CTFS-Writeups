# TP FINAL DSA 2024

Desafio web: “CTF Drunken Website”.  URL: [🚩 HACK HAVOC 🚩 (cybermaterial.com)](http://edition1.ctf.cybermaterial.com/challenges#Drunken%20website%20-23)

URL: [HACKHAVOC CTF \- 개발자는 취했습니다\! (cybermaterial.com)](http://challenge.ctf.cybermaterial.com/dissssissssimpul/)

### **Writeup Completo: CTF Drunken Website**

#### **Desafío:**

Interactuamos con una página web caótica donde debemos encontrar una flag en formato `CM{string}`. El sitio está desordenado, con varias secciones ocultas e invisibles.

#### **Pasos:**

1. **Inspección del código fuente:** Comenzamos revisando el código fuente de la página principal y encontramos un comentario:  
   html

| \<\!-- Footer with hidden section for fun \--\> |
| :---- |

   Esto indicaba una sección oculta al final de la página.

2. **Revelar la sección oculta:** Usando las herramientas de desarrollo del navegador para inspeccionar el CSS. Encontramos una clase llamada `.hidden-section`, que tenía la propiedad `display: none`. Cambiamos esta propiedad a `display: block;` para hacer visible la sección oculta.  
3. **Interacción con los botones:** Al hacer clic en cualquier botón dentro de esta sección, fuimos redirigidos a una nueva URL:

| http://challenge.ctf.cybermaterial.com/dissssissssimpul/homepage.html\# |
| :---- |

   

4. **Revisión del código fuente de la nueva página:** Inspeccionamos nuevamente el código fuente de esta página y encontramos un botón invisible:

| \<a href="/dissssissssimpul/0.html" class="invisible-button"\>Invisible Button\</a\> |
| :---- |

   Accedimos a la URL que este botón apuntaba, que nos llevó a otra página oculta.

5. **Localización de la flag:** En esta nueva página, revisamos el código fuente y encontramos un párrafo con la flag oculta, el cual tenía la clase (`.hidden-text`), al quitarla, obtenemos en el navegador el mensaje con la flag:

| \<p class="hidden-text"\>   Well, I guess I'll be fired in the morning for making such an amazing website. But you can get this flag. CM{W3bs1t3\_15\_5hi7}\</p\> |
| :---- |

   

   **Flag obtenida:** La flag es: `CM{W3bs1t3_15_5hi7}`.

# Vulnerabilidades explotadas

**Insecure DOM Manipulation** (Manipulación Insegura del DOM):

* **Descripción**: La flag estaba oculta en el código fuente del HTML utilizando la clase CSS `.hidden-text`, pero no había ninguna medida de seguridad en el backend que impidiera que el contenido fuese accesible por quien inspeccionara el HTML. Esto es un problema de seguridad en el front-end, donde el contenido sensible no debería depender exclusivamente de reglas CSS para estar protegido.  
  Además, La página contenía un botón con la clase `.invisible-button` que redirigía a una URL oculta. Este botón estaba disponible en el HTML, aunque no era visible en la interfaz. Este tipo de implementación permite que usuarios puedan interactuar con enlaces ocultos, aunque no estén visibles, lo cual podría llevar al acceso a recursos no autorizados.

**Comment Disclosure** (Divulgación de Comentarios):

* **Descripción**: El comentario HTML `<!-- Footer with hidden section for fun -->` daba indicios claros de que existía una sección oculta en la página, lo que facilitó el proceso de búsqueda. Aunque los comentarios en el código no son visibles para el usuario final, exponer este tipo de información en el código fuente puede dar pistas a los atacantes sobre contenido sensible o rutas adicionales.  
* **Impacto**: Los comentarios en el código fuente pueden ser usados por los atacantes para obtener información sobre el funcionamiento interno de la aplicación o el sitio web, lo que reduce la seguridad y facilita ataques de enumeración o explotación.

**Broken of Access Control** (Falta de Control de Acceso):

* **Descripción**: Aunque se escondían ciertos elementos en la interfaz, no se implementó ningún mecanismo de autenticación para restringir el acceso a las URLs asociadas. Cualquier usuario que conociera el enlace podría acceder al contenido oculto sin necesidad de pasar por ningún sistema de autenticación.