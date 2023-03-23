from tqdm import tqdm
import requests

# URL
url_a = "https://pwnme.org/"

# url diccionario de directorios
url_d = "https://raw.githubusercontent.com/daviddias/node-dirbuster/master/lists/directory-list-1.0.txt"

# descargar el diccionario
r = requests.get(url_d)

directory_list = "directory-list-1.0.txt"

with open(directory_list, 'wb') as f:
        # You will get the file in base64 as content
        f.write(r.content)

# Las próximas lineas de código pueden ser cambiadas por las siguientes,
# para una ejecución completa del listado de directorios

# n_words = len(list(open(directory_list, "rb")))
# print("Total directories to test:", n_words)

# with open(directory_list, "rb") as directory_list:
#     for word in tqdm(directory_list, total=n_words, unit="word"):
#         try:
#             request = requests.get(f'{url_a}{word.strip()}')
#         except:
#             continue
#         else:
#             if(request.headers['Content-Type'] == "text/plain"):
#                 print("[+] Flag found:", request.content)
#                 exit(0)
# print("[!] Not found, try other wordlist.")

# obtener un numero más reducido de directorios a probar
def prepare(wordlist,numOfChunks):
    with open(wordlist,'r') as w:
            myList=w.readlines()
    for i in range(0, len(myList), numOfChunks):
        l = myList[i:i + numOfChunks]
        if "toolkits\n" in l:
            return l

words = prepare(directory_list, 100)

# cantidad de palabras en el diccionario 
n_words = len(words)

# imprime el número total de contraseñas a probar
print("Total directories to test:", n_words)

for word in tqdm(words, total=n_words, unit="word"):
    try:
        request = requests.get(f'{url_a}{word.strip()}')
    except:
        continue
    else:
        if(request.headers['Content-Type'] == "text/plain"):
            print("[+] Flag found:", request.content.strip())
            exit(0)
print("[!] Not found, try other wordlist.")