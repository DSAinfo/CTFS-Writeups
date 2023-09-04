![img_1](https://github.com/emilianosecchi/CTFS-Writeups/assets/49136614/dfda661c-c4a5-498a-b4e1-bed678cd1ae5)

Lo que intentamos en un principio fue utilizar la herramienta autopsy pensando que lo que recibíamos era una partición de disco, donde podía haber quedado la información eliminada y teníamos que recuperarla. Luego nos dimos cuenta que esto no era correcto, ya que recibíamos una carpeta comprimida donde no podían quedar restos de los mensajes eliminados. 
Lo que pasamos a hacer fue ver cómo los teléfonos con android manejan los sms, y vimos que almacenan toda la información en una base de datos SQLite. Encontramos que la base se encuentra en el directorio:
/data/data/com.android.providers.telephony/databases/mmssms.db
Utilizamos el comando “strings mmssms.db” para imprimir todo el contenido legible del archivo y encontramos el flag como se muestra a continuación:

![img_2](https://github.com/emilianosecchi/CTFS-Writeups/assets/49136614/ccc6f967-c207-41cf-85dc-8dcb27e96201)
