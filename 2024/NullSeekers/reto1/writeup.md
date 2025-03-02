# TP FINAL FORENSIA 2024

Desafio forensia: “Broken Secrets”. URL: [ACE CTF](https://acectf.tech/challenges#Broken%20Secrets-21)

### **Writeup Completo: Broken Secrets**

#### **Desafío:**

Has encontrado un archivo sospechoso, pero parece roto y no puede abrirse con normalidad. Tu objetivo es descubrir sus secretos.

#### **Pasos:**

1. **Extraer el archivo comprimido:** Comenzamos extrayendo el archivo `Brokenfr.7z` previamente descargado utilizando la herramienta `7z`.

   ```shell
   7z x Brokenfr
   ```


2. **Navegar al directorio extraído:** Cambiamos al directorio extraído.

   ```shell
   cd _
   ```

3. **Navegar a la carpeta donde está el archivo sospechoso:** Nos dirigimos a la carpeta word/media donde se encuentra el archivo sospechoso.

   ```shell
   cd word/media
   ```

4. **Renombrar el archivo sospechoso a formato PNG** Copiamos el archivo not_so_suspicious_file y lo renombramos a suspicious.png.

   ```shell
   cp not_so_suspicious_file suspicious.png
   ```

5. **Arreglar la cabecera del archivo PNG** Utilizamos printf y dd para corregir la cabecera del archivo PNG.

   ```shell
   printf "\x89PNG\r\n\x1a\n" | dd of=suspicious.png bs=1 conv=notrunc
   ```

6. **Abrir la imagen reparada:** Finalmente, abrimos la imagen reparada para visualizar su contenido.

   ```shell
   xdg-open suspicious.png
   ```

#### **Flag obtenida::**
ACECTF{h34d3r_15_k3y}