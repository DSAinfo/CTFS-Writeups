## Writeup:autopsia de paquete modelo (H7CTF 2026)
## Análisis paso a paso

## 1. Inspección inicial y primeros pasos
Cuando descargué y descomprimí el archivo "sentiment-distilbert-meridian.zip", me encontré con tres archivos en la carpeta:
- `config.json` (la configuración del modelo)
- `README.md` (las notas del desarrollador)
- `pytorch_model.bin` (el archivo de pesos)

Lo primero que hice fue abrir el `README.md`. Ahí vi que sugería cargar el modelo con un script básico de PyTorch usando `torch.load()` y consultar una precisión (`val_accuracy`). Como el enunciado del reto decía que el operador había dejado algo fuera del registro de cambios, decidí probar esa carga en mi entorno para ver qué pasaba.

## 2. El error al intentar cargar el modelo
Armé un comando rápido en la terminal para cargar el binario, pero me devolvió este error:

NameError: name 'OPERATOR' is not defined

esto llamó mucho mi atención ya que por dentro intentaba ejecutar una función interna que dependia de una variable llamada OPERATOR que el error me aclaraba que no existia.

## 3.Investigando el archivo por dentro (Estructura ZIP)
Para no correr el riesgo de ejecutar un pickle malicioso en mi máquina, decidí revisar el archivo de forma estática. Investigué  que los formatos modernos de PyTorch en realidad son contenedores ZIP, así que lo verifiqué y comprobé que era cierto.

Dentro del ZIP encontré el archivo de metadatos principal:

pytorch_model/data.pkl


## 4. Extracción de cadenas y hallazgo del payload
Para leer el contenido de data.pkl sin ejecutarlo, escribí un script en Python (solve.py) que abriera el archivo y me listara todas las cadenas de texto legibles. Al revisar la salida, me encontré  con esto al final del archivo:

_extra_stateq>c__builtin__
eval
q?Xh
exec(__import__('zlib').decompress(__import__('base64').b64decode('...')).decode())
Al parecer,el operador había guardado un bloque de código comprimido con zlib y codificado en base64 dentro del atributo _extra_state, y lo ejecutaba usando eval y exec. Por esa razón fallaba el torch.load original.

## 5. Desofuscación y obtención de la Flag
Para ver qué hacía ese payload utilicé la siguiente línea en la terminal para decodificarlo sin correr el código:

Bash
python3 -c "import base64, zlib; payload = '...'; print(zlib.decompress(base64.b64decode(payload)).decode())"
Cuando ejecuté el comando, me devolvió el script oculto del agente de Meridian con la variable que estaba buscando:
# meridian-ml build agent :: post-load hook (do not ship)
import os, urllib.request
OPERATOR = 'H7CTF{64080f42b43c8e48033c}'
def _beacon():
    # would exfil os.environ + host info to the operator relay; neutered in this build
    return OPERATOR
_beacon()
## Conclusión
El reto estuvo genial, me paració buenisimo para entender los riesgos de seguridad al deserializar modelos de Machine Learning. Mediante inspección estática del ZIP y decodificación de bytes, pude extraer la bandera H7CTF{64080f42b43c8e48033c} sin necesidad de comprometer mi entorno ejecutando un pickle inseguro.