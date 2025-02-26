# Function to rotate string by n characters
def rotate_string(s, n):
    result = []
    for char in s:
        if char.isalpha():  # Rotate only alphabetic characters
            if char.islower():
                result.append(chr((ord(char) - ord('a') + n) % 26 + ord('a')))
            elif char.isupper():
                result.append(chr((ord(char) - ord('A') + n) % 26 + ord('A')))
        else:
            result.append(char)  # Leave non-alphabetic characters unchanged
    return ''.join(result)

target_password = "ZJPB{e6g180g9f302g8d8gddg1i2174d0e212}"

target_prefix = "WGMY"

# Function to find the ROT that decodes the target password and starts with the target prefix
def find_rot(target_password, target_prefix):
    for rot in range(26):  # Try all possible ROT values
        rotated = rotate_string(target_password, rot)
        if rotated[:4] == target_prefix:  # If the prefix matches
            return rot, rotated
    return None, None # No ROT found

# Find the ROT that decodes the target password and starts with the target prefix
rot, decoded_password = find_rot(target_password, target_prefix)

if rot is not None:
    print(f"ROT encontrado: {rot}")
    print(f"Contraseña decodificada: {decoded_password}")
else:
    print("No se encontró un ROT que cumpla con el prefijo objetivo.")
