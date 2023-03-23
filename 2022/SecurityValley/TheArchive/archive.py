from urllib.request import urlopen
from io import BytesIO
from zipfile import ZipFile
from tqdm import tqdm
import requests

# The Archive URL
url_a = "https://github.com/SecurityValley/PublicCTFChallenges/raw/master/miscellaneous/the_archive/archive.zip"

# obtener el archivo .zip
response_a = urlopen(url_a)
zip_file = ZipFile(BytesIO(response_a.read()))

# url diccionario de contraseñas
url_wl = "https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt"

# descargar el diccionario
r = requests.get(url_wl)

wordlist = "rockyou.txt"

with open(wordlist, 'wb') as f:
        # You will get the file in base64 as content
        f.write(r.content)

# cantidad de palabras en el diccionario 
n_words = len(list(open(wordlist, "rb")))

# imprime el número total de contraseñas a probar
print("Total passwords to test:", n_words)

with open(wordlist, "rb") as wordlist:
    for word in tqdm(wordlist, total=n_words, unit="word"):
        try:
            zip_file.extractall(pwd=word.strip())
        except:
            continue
        else:
            with open('flag.txt', 'r') as f:
                print("[+] Flag:", f.read())
            exit(0)
print("[!] Password not found, try other wordlist.")