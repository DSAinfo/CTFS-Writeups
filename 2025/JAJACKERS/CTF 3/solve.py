# Para ejecutar el script es necesario contar con la librería lz4
# pip install lz4


import os
import re
import lz4.block

def solve():
    # Ruta relativa al archivo recovery.jsonlz4 del perfil extraído
    jsonlz4_path = os.path.join("k-vance-profile", "sessionstore-backups", "recovery.jsonlz4")
    
    if not os.path.exists(jsonlz4_path):
        print(f"[-] Error: No se encontró el archivo en la ruta '{jsonlz4_path}'. Verifique que el ZIP esté descomprimido.")
        return

    print(f"[*] Leyendo el archivo de sesión: {jsonlz4_path}")
    with open(jsonlz4_path, "rb") as f:
        content = f.read()

    # Descomprimir el bloque LZ4 omitiendo los 8 bytes de cabecera de Firefox ('mozLz40\0')
    magic_header = content[:8]
    compressed_data = content[8:]
    
    print("[*] Descomprimiendo el bloque LZ4...")
    decompressed_bytes = lz4.block.decompress(compressed_data)
    json_str = decompressed_bytes.decode('utf-8', errors='ignore')

    # Buscar el patrón de la flag usando expresiones regulares
    print("[*] Buscando la flag dentro del JSON de la sesión...")
    flag_match = re.search(r'POCTF\{[^}]+\}', json_str)
    
    if flag_match:
        print(f"\n[SUCCESS] Flag encontrada: {flag_match.group(0)}")
    else:
        print("[-] No se encontró ninguna flag con el formato POCTF{...}")

if __name__ == "__main__":
    solve()