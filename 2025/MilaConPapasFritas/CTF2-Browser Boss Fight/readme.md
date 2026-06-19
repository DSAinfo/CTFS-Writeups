
# Browser Boss Fight-WriteUp
## Categoría: Web

### Descripción del desafío:

### El desafío nos presenta una página con solo un input para ingresar una “key”.

<img width="1365" height="728" alt="image1-bbf" src="https://github.com/user-attachments/assets/d174ec2d-785e-4953-984c-cef34d58b6f6" />





### Si inspeccionamos el código, observamos que no importa cual sea el input  ingresado, el valor del input se cambia a  “WEAK_NON_KOOPA_KNOCK”.

<img width="1365" height="729" alt="image2-bbf" src="https://github.com/user-attachments/assets/e9579253-2d4e-416c-8061-534f24118fa8" />



### Si probamos cualquier input obtenemos el siguiente mensaje en pantalla. Ademas podemos visualizar la cabecera “server” que contiene una pista : “In case you forget the key, check under_the_mat”
<img width="1331" height="438" alt="image3-bbf" src="https://github.com/user-attachments/assets/6adc49e0-d7ed-4fb7-8a8f-4469e7754d40" />


### Ahora haciendo uso de burp suite y de la pista, interceptamos la peticion para cambiar el valor constante de key por “under_the_mat”.
<img width="1365" height="724" alt="image4-bbf" src="https://github.com/user-attachments/assets/f70d8912-659a-4d94-aced-21db724c4e24" />

### Y asi logramos el acceso a la siguiente pagina:
<img width="1355" height="657" alt="image5-bbf" src="https://github.com/user-attachments/assets/662ba8a2-dac2-41ad-88c6-165144b97f42" />

### Como vemos el texto dice “i removed the axe”, si inspeccionamos encontramos que tiene hasAxe=false:
<img width="1007" height="101" alt="image6-bff" src="https://github.com/user-attachments/assets/8703de20-df5f-4ec2-93ac-7cc4f510d895" />

### Si interceptamos nuevamente la petición get y modificamos el valor por true:
<img width="1365" height="728" alt="image7-bbf" src="https://github.com/user-attachments/assets/10928b82-bd9e-4c2b-a62e-aff04d60a94c" />


### Finalmente obtenemos la flag:
<img width="1365" height="728" alt="image8-bbf" src="https://github.com/user-attachments/assets/015f165a-48bc-499d-a589-2ca5bce7b413" />

## Flag obtenida : UMASS{br0k3n_1n_2_b0wz3r5_c4st13}

