import rsa
from sympy import factorint

# Clave pública
e = 5
n = 14537813

# Factorización de n para obtener p y q (primos que componenen a 'n')
factors = factorint(n)
p = list(factors.keys())[0]
q = list(factors.keys())[1]

# Calculo de d (inverso multiplicativo de e mod phi(n))
phi_n = (p - 1) * (q - 1)
d = pow(e, -1, phi_n)

# Calculo la clave privada
private_key = rsa.PrivateKey(n, e, d, p, q)

# Mensaje encriptado
encrypted_message = [13831133, 12917356, 10030587, 10030587, 7776496, 10814604, 
                     6081412, 10030587, 12646311, 9767093, 8851505, 7850875, 256117, 
                     13831133, 11803398, 7205927, 2220894, 12646311, 6081412, 
                     10030587, 2170797, 11065575, 13799515, 12522469, 2708638]
decrypted_message = ""
for i in encrypted_message:
    encrypted_message_bytes = i.to_bytes(
        (i.bit_length() + 7) // 8, 'big') 
    # Se descifra letra por letra el mensaje
    decrypted_letter = rsa.decrypt(encrypted_message_bytes, private_key)
    decrypted_message = decrypted_message + decrypted_letter.decode()
print("Flag: " + decrypted_message)