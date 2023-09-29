import subprocess

file_pcap = "recurso/captured_packets.pcapng"
file_master_keys_tls = "recurso/master_keys.log"
packet_number = 72

cmd = f"tshark -r {file_pcap} -Y 'frame.number == {packet_number}' -o tls.keylog_file:{file_master_keys_tls} -V | grep uctf"
result = subprocess.check_output(cmd, shell=True, universal_newlines=True)
print(result)
