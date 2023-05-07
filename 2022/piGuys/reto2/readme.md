# Writeup: Solución al challenge icsjwgctf 2023 | ICS & Security Basics

Se trata de una serie de challenges que hay que resolver para obtener la flag

## Challenge 1

Primer challenge, nos hace buscar el mensaje oculto en el código fuente. Rápidamente lo descubrimos: 
<img width="1529" alt="image" src="https://user-images.githubusercontent.com/25467138/236702994-0f06ca27-b04b-4e0c-8757-daa2aed72574.png">

## Challenge 2

Nos pide buscar la url que no desea que los robots crawleen.
<img width="1477" alt="image" src="https://user-images.githubusercontent.com/25467138/236703007-d4982de7-a40d-40a8-badd-fc1a17c91b94.png">

Para esto, las páginas webs incluyen un archivo "robots.txt". Entramos a esa url.

<img width="1477" alt="image" src="https://user-images.githubusercontent.com/25467138/236703037-ac7e95ed-9340-43dc-9e5d-bc99fe9a05da.png">

Luego, entrando a la url /nothing_to_see_here, podemos ver el mensaje oculto.

<img width="1477" alt="image" src="https://user-images.githubusercontent.com/25467138/236703049-f3dfa1e7-3c4d-4a27-a309-9f63441b64aa.png">

## Challenge 3

Nos dan la siguiente pista

<img width="630" alt="Screenshot 2023-05-07 at 23 03 56" src="https://user-images.githubusercontent.com/25467138/236702459-d4ccc8af-1aa1-47a6-97fe-9bb1d95874c7.png">

## Solución:

El mensaje que debemos enviar para obtener el reto nos lo dan: "this is easy", sin embargo, hay un input de tipo number del 0 al 1000.

<img width="643" alt="Screenshot 2023-05-07 at 23 05 15" src="https://user-images.githubusercontent.com/25467138/236702503-b9869813-61ef-4eb3-b7f8-858e3cd86cb6.png">

Procedemos a editar el html del input, cambiandolo a un input de tipo texto, para poder colocar el texto.

<img width="635" alt="Screenshot 2023-05-07 at 23 05 50" src="https://user-images.githubusercontent.com/25467138/236702523-35248d8a-4a4f-4941-bbd9-bda386b77708.png">

Por último, enviamos el mensaje.

<img width="624" alt="Screenshot 2023-05-07 at 23 06 56" src="https://user-images.githubusercontent.com/25467138/236702567-5f624339-f9c2-493b-8932-8e83a92aa2c6.png">

## Challenge 4

<img width="1216" alt="Screenshot 2023-05-07 at 23 08 08" src="https://user-images.githubusercontent.com/25467138/236702616-209de28a-9b1a-42d1-ae02-05293c54cadb.png">

Observamos las cookies y vemos dos que pertenecen al dominio, una es un booleano y otra un hash. 
Tomamos el hash (c2680ace859ea7a827362d1b) y lo "bakeamos" en CyberChef para obtener el mensaje secreto.
Entonces, tomamos la cookie que dice show_message: false, y la colocamos en true.

<img width="1529" alt="Screenshot 2023-05-07 at 23 13 23" src="https://user-images.githubusercontent.com/25467138/236702804-f1bc7363-4062-4b67-9ee4-3b120ddb32ff.png">

Copiamos la request, y la pegamos en postman. 

<img width="1477" alt="Screenshot 2023-05-07 at 23 14 10" src="https://user-images.githubusercontent.com/25467138/236702844-f0e4bc75-ef9e-45ba-9193-031f90a42dc9.png">

<img width="1792" alt="image" src="https://user-images.githubusercontent.com/25467138/236702916-90dc61ca-536f-4ac8-9a6e-1453eae4180e.png">

Y obtenemos el mensaje.

<img width="1792" alt="image" src="https://user-images.githubusercontent.com/25467138/236702925-5321e505-0b2c-4c84-aa4b-3e421aab5276.png">

## Flag

Por último, obtenemos la flag.

<img width="1529" alt="image" src="https://user-images.githubusercontent.com/25467138/236702950-7748946c-939b-47f9-9a54-fee076b1917c.png">

`flag{JTc0JTc1JTcyJTc0JTc3JTY5JTY3}`

## Conclusión

Este reto está compuesto por 4 sub-retos con ejercicios similares a los vistos en la práctica de la materia.

*Enlace: [http://challenges.icsjwgctf.com:8000/web](http://challenges.icsjwgctf.com:8000/web)*
