import tarfile
import os
import requests
from tqdm import tqdm

resource_url = "https://cdn.2024.irisc.tf/whats-a-rune.tar.gz"

RESOURCE1_PATH = "./recurso/whats-a-rune.tar.gz"
SOLVE_FILES_PATH = "./solve"

def write_flag_to_file(flag, flag_file_path):
    with open(flag_file_path, 'w') as flag_file:
        flag_file.write(flag)
    print(f'[+] Flag written to {flag_file_path}')

# Check if the resource already exists
if not os.path.exists(RESOURCE1_PATH):
    # If the file doesn't exist, download it
    try:
        # Create the 'recurso' directory if it doesn't exist
        os.makedirs(os.path.dirname(RESOURCE1_PATH), exist_ok=True)
        
        # Download the file
        print(f"[+] Downloading file {RESOURCE1_PATH} from {resource_url}")
        # Download the file with tqdm for progress bar
        response = requests.get(resource_url, stream=True)
        total_size = int(response.headers.get('content-length', 0))

        with open(RESOURCE1_PATH, "wb") as file, tqdm(
            desc="Downloading",
            total=total_size,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for data in response.iter_content(chunk_size=1024):
                bar.update(len(data))
                file.write(data)
        
        print(f"[+] File downloaded to {RESOURCE1_PATH}")
    except Exception as e:
        print(f"[-] Failed to download the file. Error: {e}")
else:
    print(f"[+] The file {RESOURCE1_PATH} already exists. Skipping download")

# Extract the challenge resource using tarfile
try:
    print(f"[+] Extracting file {RESOURCE1_PATH}")
    with tarfile.open(RESOURCE1_PATH, 'r:gz') as tar:
        tar.extractall(SOLVE_FILES_PATH)
    print(f'[+] Extraction of file {RESOURCE1_PATH} successful')
    print()

except Exception as e:
    print(f"[-] Error during extraction: {e}")

# Read encoded flag from file
file_path = SOLVE_FILES_PATH + "/whats-a-rune/the"

with open(file_path, "r", encoding='utf-8') as file:
    flag = file.read().strip()

# Reverse the transformation
runed = []
z = 0

for v in flag:
    runed.append(chr(ord(v) - z))
    z = ord(v) - z

# Reconstruct the original string
result = ''.join(runed)

# Extract the flag
flag = result.split('}')[0] + '}'

# Print the flag
print("[+] Flag:", flag)

# Write flag to file
# Create the solve directory if it doesn't exist
if not os.path.exists(SOLVE_FILES_PATH):
    os.makedirs(SOLVE_FILES_PATH)

write_flag_to_file(flag, SOLVE_FILES_PATH + "/flag.txt")
