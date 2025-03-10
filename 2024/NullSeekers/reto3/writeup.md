# TP FINAL FORENSIA 2024

Desafío forensia: “Tabs and Spaces”. URL: [ACE CTF](https://acectf.tech/challenges#Tabs&Spaces-30)

### **Writeup Completo: Tabs and Spaces**

#### **Desafío:**

Se ha descubierto un misterioso archivo ZIP que contiene una colección de imágenes y un archivo. La tarea consiste en recuperar la bandera.

#### **Pasos:**

1. Descargamos el archivo `Tabsspaces.zip`.
2. Extraemos el contenido usando `unzip recurso/Tabsspaces.zip -d extract`.
3. Cambiamos al directorio donde están los archivos con `cd extract/ctf/files`.
4. Calculamos los checksums de los archivos ocultos y los guardamos en un archivo.
5. Ordenamos y contamos los checksums únicos, luego filtramos el que aparece solo una vez.
6. Extraemos datos ocultos de la imagen sospechosa con ```steghide extract -sf ". $file_different" -p "" -f. ```
7. Convertimos espacios y tabulaciones a binario.
8. Convertimos binario a ASCII
9. Obtenemos la flag

#### **Flag obtenida:**
ACECTF{n0_3xp1017_n0_g41n}

