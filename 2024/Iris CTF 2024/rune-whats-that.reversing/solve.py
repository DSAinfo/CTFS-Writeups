# File: solve.py
# Author: Julián Casaburi
# Date: January 6, 2024
# Description: This is a script to solve the challenge "Rune? What's that? (Iris CTF 2024 - Reverse Engineering)".

import tarfile
import os
import requests
from tqdm import tqdm

resource_url = "https://cdn.2024.irisc.tf/whats-a-rune.tar.gz"

RESOURCE1_PATH = os.path.join(".", "recurso", "whats-a-rune.tar.gz")
SOLVE_FILES_PATH = os.path.join(".", "solve")
file_path = os.path.join(SOLVE_FILES_PATH, "whats-a-rune", "the")
flag_file_path = os.path.join(SOLVE_FILES_PATH, "flag.txt")


def write_flag_to_file(flag, flag_file_path):
    with open(flag_file_path, "w") as flag_file:
        flag_file.write(flag)
    print(f"[+] Flag written to {flag_file_path}")


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
        total_size = int(response.headers.get("content-length", 0))

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
    with tarfile.open(RESOURCE1_PATH, "r:gz") as tar:
        tar.extractall(SOLVE_FILES_PATH)
    print(f"[+] Extraction of file {RESOURCE1_PATH} successful")
    print()

    # Read encoded flag from file
    with open(file_path, "r", encoding="utf-8") as file:
        flag = file.read().strip()

    # Reverse the transformation
    runed = []
    z = 0

    print("[+] Reversing transformation")
    with tqdm(total=len(flag), desc="Progress", unit="char") as bar:
        for v in flag:
            runed.append(chr(ord(v) - z))
            z = ord(v) - z
            bar.update(1)

    # Reconstruct the original string
    result = "".join(runed)

    # Extract the flag
    flag = result.split("}")[0] + "}"

    # Print the flag
    print("[+] Flag:", flag)

    # Write flag to file
    # Create the solve directory if it doesn't exist
    if not os.path.exists(SOLVE_FILES_PATH):
        os.makedirs(SOLVE_FILES_PATH)

    write_flag_to_file(flag, flag_file_path)

except Exception as e:
    print(f"[-] Error during extraction: {e}")
