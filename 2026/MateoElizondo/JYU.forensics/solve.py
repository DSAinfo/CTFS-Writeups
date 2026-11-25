from scapy.all import rdpcap, TCP
import pynvim

# Este script espera encontrar el archivo "secret.pcap" en la carpeta de recursos
# Requiere tener neovim instalado en el sistema y la librería pynvim

packets = rdpcap("recursos/secret.pcap")

result = ""

for pkt in packets:

    # Se queda solo con la conexión por donde el cliente envía los inputs
    if not pkt[TCP].sport == 56243:
        continue

    if TCP in pkt:
        payload = bytes(pkt[TCP].payload)

        if payload:
            # Ignora los inputs del usuario que no son bytes individuales
            if len(payload) > 1:
                continue

            # 3a es ':'
            # En la captura, la única vez que el cliente ingresa ':' es para ejecutar wq
            # Entonces sabemos que es la línea de corte para guardar los inputs de vi
            if payload.hex() == '3a':
                break

            # 7f es DEL. Después de evaluar quedaba el byte '7f' escrito en vez borrar el anterior
            # Esto lo borra manualmente
            if payload.hex() == '7f':
                result = result[0:len(result)-5]
                continue
        result += " "+payload.hex()

# Ejecuta el entorno de nvim y evalua la expresión
nvim = pynvim.attach(
    'child',
    argv=['nvim', '--embed', '--headless', '--clean']
)
nvim.input(bytes.fromhex(result))
nvim.eval("1")
dvmsg = "".join(nvim.current.buffer[:])

# dvorak -> qwerty
qwerty = "qQwWeErRtTyYuUiIoOpP[{]}sSdDfFgGhHjJkKlL;:\"zZxXcCvVbBnN,<.>/?=_+-"
dvorak = "'\",<.>pPyYfFgGcCrRlL/?=+oOeEuUiIdDhHtTnNsS_;:qQjJkKxXbBwWvVzZ]{}["

translation_table = str.maketrans(dvorak, qwerty)
print(dvmsg.translate(translation_table))

