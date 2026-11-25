from scapy.all import rdpcap, TCP, IP

# Este script espera encontrar el archivo "capture.pcap" en la carpeta de recursos
# También requiere tener la librería de scapy

# El script relaciona la cantidad de mensajes enviados en ráfagas y el tiempo transcurrido para extraer la flag en morse y decodificarla
# Las señales fueron determinadas a prueba y error de la siguiente manera:
# Si aparece una pausa de al menos 0.08s se revisa la cantidad de mensajes enviados
# -> Si la cantidad de mensajes es entre 4 y 14 la señal es punto
# -> Si es entre 15 y 40, es línea
# Además de la señal, si la pausa se alarga más de 0.12, hay que insertar un espacio


packets = rdpcap("recursos/capture.pcap")

last_time = None
i = 0
result = ""

for pkt in packets:
    if not TCP in pkt:
        continue

    # Filtro por el puerto para IRC y la dirección que tiene el mensaje correcto
    if pkt[TCP].sport == 6667 and pkt[IP].dst == "192.168.1.23":
        current_time = float(pkt.time)
        if last_time is not None:
            
            delta = current_time - last_time

            if delta > 0.08:
                if i > 4 and i < 15:
                    result += "."
                elif i > 14 and i < 40:
                    result += "-"
                if delta > 0.12 and delta < 1.0:
                    result += " "
                i = 0
            else:
                i += 1
    # El codigo morse aparece dos veces seguidas en el pcap
    # En el medio hay una pausa bastante mas larga que las otras, este break es para quedarnos solo con el primero
            if delta > 1.5:
                break
        last_time = current_time 


MORSE_CODE_DICT = {
    '.-': 'A',
    '-...': 'B',
    '-.-.': 'C',
    '-..': 'D',
    '.': 'E',
    '..-.': 'F',
    '--.': 'G',
    '....': 'H',
    '..': 'I',
    '.---': 'J',
    '-.-': 'K',
    '.-..': 'L',
    '--': 'M',
    '-.': 'N',
    '---': 'O',
    '.--.': 'P',
    '--.-': 'Q',
    '.-.': 'R',
    '...': 'S',
    '-': 'T',
    '..-': 'U',
    '...-': 'V',
    '.--': 'W',
    '-..-': 'X',
    '-.--': 'Y',
    '--..': 'Z',
    '.----': '1',
    '..---': '2',
    '...--': '3',
    '....-': '4',
    '.....': '5',
    '-....': '6',
    '--...': '7',
    '---..': '8',
    '----.': '9',
    '-----': '0',
    '..--.-': '_',
}
dec = ""
for code in result.split():
    dec += MORSE_CODE_DICT[code]

print("cruXipher{"+dec+"}")
