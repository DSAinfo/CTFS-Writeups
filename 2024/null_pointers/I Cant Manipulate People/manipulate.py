from scapy.all import rdpcap, ICMP

def extract_icmp_hex(pcap_file):	
    packets = rdpcap(pcap_file)
    hex_sequence = ""

    for packet in packets:
        # Check if the packet has ICMP layer and is an echo request
        if packet.haslayer(ICMP) and packet[ICMP].type == 8:
            # Extract data from the ICMP layer
            icmp_data = bytes(packet[ICMP].payload)
            # Convert the data to hex and append it to the sequence
            hex_sequence += icmp_data.hex()

    return hex_sequence

def hex_to_ascii(hex_sequence):

    bytes_object = bytes.fromhex(hex_sequence)
    return bytes_object.decode("utf-8", errors="ignore")

# Path to the PCAP file
pcap_file = "capture.pcap"  # Replace with your PCAP file

# Extract hex sequence from ICMP packets
hex_sequence = extract_icmp_hex(pcap_file)
print(f"Hex Sequence: {hex_sequence}")

# Convert hex sequence to ASCII to reveal the flag
ascii_flag = hex_to_ascii(hex_sequence)
print(f"Flag: {ascii_flag}")
