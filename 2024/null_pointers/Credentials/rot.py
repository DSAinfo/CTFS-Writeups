# Función para realizar ROT-n en una cadena de texto
def rotate_string(s, n):
    result = []
    for char in s:
        if char.isalpha():  # Rotar solo caracteres alfabéticos
            if char.islower():
                result.append(chr((ord(char) - ord('a') + n) % 26 + ord('a')))
            elif char.isupper():
                result.append(chr((ord(char) - ord('A') + n) % 26 + ord('A')))
        else:
            result.append(char)  # Dejar los caracteres no alfabéticos como están
    return ''.join(result)

# Contraseña objetivo
target_password = "ZJPB{e6g180g9f302g8d8gddg1i2174d0e212}"

# Prefijo objetivo
target_prefix = "WGMY"

# Función para encontrar el ROT correcto
def find_rot(target_password, target_prefix):
    for rot in range(26):  # Probar ROTs de 0 a 25
        rotated = rotate_string(target_password, rot)
        if rotated[:4] == target_prefix:  # Si las primeras 4 letras coinciden
            return rot, rotated
    return None, None  # Si no se encuentra un ROT válido

# Ejecutar la búsqueda
rot, decoded_password = find_rot(target_password, target_prefix)

# Mostrar el resultado
if rot is not None:
    print(f"ROT encontrado: {rot}")
    print(f"Contraseña decodificada: {decoded_password}")
else:
    print("No se encontró un ROT que cumpla con el prefijo objetivo.")
