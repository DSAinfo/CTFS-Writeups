
import subprocess


def proccess():
    command="steghide extract -sf recurso/3AW-Memes.jpg;cat adj.txt;rm adj.txt"
    result = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    return result.stdout.read()

print("este script toma por ejemplo imprime le flag")
print(proccess())
