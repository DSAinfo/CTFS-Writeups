import subprocess
import binascii

file_pcap = "recurso/traffic.pcap"
packet_number = 254

cmd = f"tshark -r {file_pcap} -V -Y 'frame.number == {packet_number}' -T fields -e data"
packet_data_hex = subprocess.check_output(cmd, shell=True, universal_newlines=True)
byte_str = binascii.unhexlify(packet_data_hex.strip())
result = byte_str.decode("ASCII")
print(result)
