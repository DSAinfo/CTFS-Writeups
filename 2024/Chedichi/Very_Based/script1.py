import base64

# Cadena codificada en base64
base_64 = "SU5FVkk2WlhHSlJXT1MyTUdORFZFSkJFTEJSRzRLVDU="

# Decodificar la cadena en base64
base32 = base64.b64decode(base_64)

# Cadena decodificada en base64
print("Decodificado en base64:", base32)

# Decodificar la cadena en base32
flag = base64.b32decode(base32)

# Cadena decodificada en base32
print("Decodificado en base32:", flag)