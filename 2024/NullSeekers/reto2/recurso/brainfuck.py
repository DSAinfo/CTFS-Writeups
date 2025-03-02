import sys

def brainfuck_interpreter(code):
    # Puntero de memoria
    memory = [0] * 30000  # Usualmente, se utilizan 30,000 celdas de memoria
    pointer = 0
    output = []

    # Usar un índice para recorrer el código de Brainfuck
    i = 0
    while i < len(code):
        command = code[i]
        
        if command == '>':
            pointer += 1
        elif command == '<':
            pointer -= 1
        elif command == '+':
            memory[pointer] += 1
        elif command == '-':
            memory[pointer] -= 1
        elif command == '.':
            output.append(chr(memory[pointer]))  # Imprime el carácter correspondiente al valor ASCII
        elif command == ',':
            # Este código no maneja la entrada (por lo que se omite por ahora)
            pass
        elif command == '[':
            # Si el valor en la celda es cero, saltar al final del bucle
            if memory[pointer] == 0:
                open_brackets = 1
                while open_brackets != 0:
                    i += 1
                    if code[i] == '[':
                        open_brackets += 1
                    elif code[i] == ']':
                        open_brackets -= 1
        elif command == ']':
            # Si el valor en la celda no es cero, saltar de vuelta al comienzo del bucle
            if memory[pointer] != 0:
                close_brackets = 1
                while close_brackets != 0:
                    i -= 1
                    if code[i] == ']':
                        close_brackets += 1
                    elif code[i] == '[':
                        close_brackets -= 1
        i += 1

    return ''.join(output)


# Función principal que recibe el texto Brainfuck como parámetro
def ejecutar_brainfuck(texto_brainfuck):
    result = brainfuck_interpreter(texto_brainfuck)
    return result


# Código que maneja los argumentos de la línea de comandos
if __name__ == "__main__":
    if len(sys.argv) != 2:
        # Si no hay argumento, leer de stdin (como un archivo o desde un pipe)
        codigo_brainfuck = sys.stdin.read().strip()
    else:
        # Leer el archivo especificado en el argumento
        archivo = sys.argv[1]
        try:
            with open(archivo, 'r') as file:
                codigo_brainfuck = file.read().strip()
        except FileNotFoundError:
            print(f"Error: El archivo '{archivo}' no se encuentra.")
            sys.exit(1)
        except Exception as e:
            print(f"Error al leer el archivo: {e}")
            sys.exit(1)

    # Ejecutar el código Brainfuck y mostrar el resultado
    resultado = ejecutar_brainfuck(codigo_brainfuck)
    print(resultado)
