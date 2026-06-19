import base64

# Leer el contenido del archivo
with open("secret_message.txt", "r") as f:
    data = f.read().strip()

# Decodificar hasta 50 veces
for i in range(50):
    try:
        # Decodificar
        data = base64.b64decode(data).decode('utf-8')
        
        # Mostrar progreso
        print(f"Capa {i+1}: {data[:50]}...")
        
        # Si encontramos la flag en formato kashiCTF, terminamos
        if data.startswith("kashiCTF{") or data.startswith("flag{"):
            print(f"\nFLAG encontrada en capa {i+1}:")
            print(data)
            break
            
    except Exception as e:
        print(f"Error en capa {i+1}: {e}")
        break
