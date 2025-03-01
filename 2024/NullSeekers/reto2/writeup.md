# TP FINAL FORENSIA 2024

Desafio forensia: “Samurai's Code”. URL: [Apoorv CTF](https://apoorvctf.iiitkottayam.ac.in/challenges#Samurai%E2%80%99s%20Code-26)

### **Writeup Completo: Samurai's Code**

#### **Desafío:**

Revela el código perdido de los samuráis y desbloquea el misterio oculto dentro.

#### **Pasos:**

1. Descargamos el archivo files.zip
2. Extraemos el contenido usando unzip recurso/files.zip -d extract
3. Cambiamos al directorio donde están los archivos con cd extract/ctf/files.
4. Se examinó el archivo sam.jpg con strings sam.jpg y se pudo encontrar una secuencia de datos extraños al final del archivo:
   ++++++++++[>+>+++>+++++++>++++++++++<<<<-]>>>>++++.++++++++++++..----.+++.<------------.-----------..>---------------.++++++++++++++.---------.+++++++++++++.-----------------.<-.>++.++++++++..--------.+++++.-------.<.>--.++++++++++++.--.<+.>-------.+++.+++.-------.<.>-.<.++.+++++++++++++++++++++++++.+++++++++++++.>+++++++++++++.<+++++++++++++.----------------------------------.++++++++.>+++++++++.-------------------.<+++++++.>+.<-----.+++++++++.------------.<+++++++++++++++.>>++++++++++++++++.<+++.++++++++.>-.<--------.---------.++++++++++++++++++++.>.<++.>--------------.<<+++++.>.>-----.+++++++.<<++.>--.<++.---------.++.>>+++++++++++.-------------.----.++++++++++++++++++.<<++++++++++++++++.>>--.--.---.<<--.>>+++.-----------.-------.+++++++++++++++++.---------.+++++.-------.

   Estos datos seguían un patrón parecido al de un código Brainfuck.
6. 
..


#### **Flag obtenida::**
apoorvctf{ByT3s_0UT_0F_0Rd3R}
