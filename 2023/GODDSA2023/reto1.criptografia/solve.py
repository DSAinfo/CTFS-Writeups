import string

flag = []

with open("message.txt") as file:
    mensaje = file.read()
    numeros = [int(val) for val in mensaje.split()]

    for numero in numeros:
        modulos = numero % 37

        if modulos in range(26):
            flag.append(string.ascii_uppercase[modulos])
        elif modulos in range(26, 36):
            flag.append(string.digits[modulos - 26])
        else:
            flag.append("_")
        
print("picoCTF{%s}" % "".join(flag))