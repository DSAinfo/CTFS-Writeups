## NullOrigin CTF Qualifiers

# Sanity - 3

**CTF:** NullOrigin CTF Qualifiers  
**Categoría:** OSINT  
**Dificultad:** Easy  
**Autor:** KUSH  
**Fecha de resolución:** 18/09/2026  
**Reto:** Sanity - 3  
**Evento:** [NullOrigin CTF Qualifiers - CTFtime](https://ctftime.org/event/3346)

![Portada del evento NullOrigin CTF Qualifiers](./imágenes/Imagen%20pegada.png)

![Descripción del reto Sanity - 3](./imágenes/Imagen%20pegada%20(2).png)

El enunciado, haciendo referencia a las reseñas, nos invita a buscar y explorar en torno a **CyberHX** para poder completar el reto.  
Por lo tanto, como primer paso realizamos una búsqueda de **CyberHX** en Google.

![Resultados de búsqueda de CyberHX](./imágenes/Imagen%20pegada%20(3).png)

Entre los resultados encontramos el perfil de **Cyberhx** el cual se ubicada en Bhopal, India, junto con sus reseñas públicas en Google.

Teniendo en cuenta la pista:

```text
Not every review is just a review.
```

Accedemos a las opiniones del perfil para comprobar si alguna nos brinda información relacionada con el reto y la obtención de la flag.

![Reseñas de Cyberhx en Google](./imágenes/Imagen%20pegada%20(4).png)
![Reseñas de Cyberhx en Google Parte 2](./imágenes/Imagen%20pegada%20(5).png)

Al revisar las distintas reseñas encontramos una respuesta publicada por el propietario de **Cyberhx** que contiene, a primera vista, una cadena codificada en Base64 (por su estructura y por el caracter `=` al final): 

```text
TnVsbDByaWdpbntBX1Izdmlld19UMF9SM20zbWIzcn0=
```
Por lo tanto, para chequearlo procedemos a utilizar la herramienta CyberChef aplicando la operación o receta `From Base64`:

![Decodificación de la cadena Base64 en CyberChef](./imágenes/Imagen%20pegada%20(6).png)

El resultado obtenido es:

```text
NullOrigin{A_R3view_T0_R3m3mb3r}
```

Finalmente, ingresamos la flag obtenida en el campo **Submit Access Key** de la plataforma, quedando resuelto el reto de forma correcta.

![Ingreso de la flag de Sanity - 3](./imágenes/Imagen%20pegada%20(7).png)

![Reto Sanity - 3 resuelto](./imágenes/Imagen%20pegada%20(8).png)
