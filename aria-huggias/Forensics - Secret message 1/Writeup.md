# Tipo: Forensics Desafío: Secret message 1
![image](https://github.com/LauAria/CTFS-Writeups/assets/48163730/cf88ae94-140b-4105-af69-647309646cd9)

Usamos la libreria de pdfminer-data quer extrae metadata de pdfs la cual nos dio la flag:
uoftctf{fired_for_leaking_secrets_in_a_pdf}

![image](https://github.com/LauAria/CTFS-Writeups/assets/48163730/84f42c57-eb8c-4a6d-944d-fe7b9a0b78bc)

Filtramos con grep para quedarnos solo con la flag.
pdf2txt secret.pdf | grep -o 'uoftctf{[^}]*}'
![image](https://github.com/LauAria/CTFS-Writeups/assets/48163730/2d791d07-4cad-4992-9839-7f9e87791818)

resolucion:

$ sudo apt install pdfminer-data

$ pdf2txt secret.pdf | grep -o 'uoftctf{[^}]*}'
