import zipfile
import re

model_path = "pytorch_model.bin"

print("[*] Analizando los metadatos internos del modelo...")

with zipfile.ZipFile(model_path, 'r') as z:
    with z.open("pytorch_model/data.pkl") as f:
        content = f.read()
        print("[*] Todas las cadenas legibles en data.pkl:")
        # Busqueda  de cualquier secuencia de caracteres imprimibles de al menos 3 caracteres evitando contenido basura
        strings = re.findall(b"[ -~]{3,}", content)
        for s in strings:
            print("   ", s.decode('utf-8', errors='ignore'))
            