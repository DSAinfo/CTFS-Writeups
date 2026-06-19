import codecs
import re

def rot47_decodificar(texto):
    resultado = []
    for char in texto:
        codigo = ord(char)
        if 33 <= codigo <= 126:  # Rango de caracteres imprimibles
            # Aplica ROT47 (desplazamiento de 47)
            nuevo_codigo = 33 + ((codigo - 33 + 47) % 94)
            resultado.append(chr(nuevo_codigo))
        else:
            resultado.append(char)  # Mantiene caracteres especiales como saltos de línea
    return ''.join(resultado)

def rot13_decodificar(texto):
    return codecs.decode(texto, 'rot_13')


def extraer_flag(texto):
    # Busca el patrón jctf{...} de la flag
    patron = r'jctf\{[^}]*\}'
    coincidencias = re.findall(patron, texto)
    
    if coincidencias:
        return coincidencias[0]
   
    return None

def decodificar_doble(archivo_entrada):
 
    with open(archivo_entrada, 'r', encoding='utf-8') as f:
        contenido = f.read() 
    # Aplica ROT47
    rot47_resultado = []
    for char in contenido:
        codigo = ord(char)
        if 33 <= codigo <= 126:
            nuevo_codigo = 33 + ((codigo - 33 + 47) % 94)
            rot47_resultado.append(chr(nuevo_codigo))
        else:
            rot47_resultado.append(char)
    
    # Aplica ROT13 al resultado de ROT47
    resultado_intermedio = ''.join(rot47_resultado)
    final = codecs.decode(resultado_intermedio, 'rot_13')
    
    return final

if __name__ == "__main__":
    archivo = "CryptoVisor.txt" 
    try:
        texto_final = decodificar_doble(archivo)
        flag = extraer_flag(texto_final)
        
        if flag:
            print(f" FLAG ENCONTRADA: {flag}")
        else:
            print("\n No se encontró flag con formato jctf{}")
            print("\nTexto completo decodificado:")
            print(texto_final)       
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{archivo}'")
    except Exception as e:
        print(f"Error durante la decodificación: {e}")