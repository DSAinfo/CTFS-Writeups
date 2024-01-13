# File: solve.py
# Author: Julián Casaburi
# Date: January 6, 2024
# Description: This is a script to solve the challenge "Where's skat? (Iris CTF 2024 - Networks)".

import requests
from tqdm import tqdm
from scapy.all import *
import tarfile
import zipfile
import os
import urllib.request
import subprocess
import webbrowser

RESOURCE_URL = "https://cdn.2024.irisc.tf/wheres-skat.tar.gz"

RESOURCE1_PATH = os.path.join(".", "recurso", "wheres-skat.tar.gz")
SOLVE_FILES_PATH = os.path.join(".", "solve")
RESOURCE2_PATH = os.path.join(SOLVE_FILES_PATH, "wheres-skat", "wheres-skat.zip")
GEOWIFI_PATH = os.path.join(SOLVE_FILES_PATH, "geowifi-main", "geowifi.py")
PCAP_FILE = os.path.join(SOLVE_FILES_PATH, "wheres-skat.pcap")

# GitHub repository URL
REPO_URL = 'https://github.com/GONZOsint/geowifi'

def extract_wifi_bssids(pcap_file):
    try:
        bssids = set()

        # Read the pcap file
        packets = rdpcap(pcap_file)

        # Extract WiFi BSSIDs from Beacon and Probe Response frames
        for packet in packets:
            if packet.haslayer(Dot11) and (packet.type == 0 or packet.type == 2):
                bssid = packet.addr3
                bssids.add(bssid)

        return bssids
    except Exception as e:
        print(f"Error extracting WiFi BSSIDs: {e}")
        return set()

def find_specific_bssids(bssids, *specific_bssids):
    try:
        found_bssids = set(specific_bssids).intersection(bssids)
        return found_bssids
    except Exception as e:
        print(f"Error finding specific BSSIDs: {e}")
        return set()
    
def download_and_extract_github_repo(repo_url, target_folder):
    # Create the target folder if it doesn't exist
    os.makedirs(target_folder, exist_ok=True)

    # Construct the URL for the ZIP file
    zip_url = f'{repo_url}/archive/refs/heads/main.zip'

    # Download the ZIP file
    with urllib.request.urlopen(zip_url) as response:
        with zipfile.ZipFile(io.BytesIO(response.read())) as zip_ref:
            # Extract the ZIP file to the target folder
            zip_ref.extractall(target_folder)

    print(f"Repository downloaded and extracted to {target_folder}")

def extract_lat_lon_from_output(output):
    for line in output.split('\n'):
        if 'apple' in line:
            parts = line.split('│')
            if len(parts) >= 6:
                lat = parts[4].strip()
                lng = parts[5].strip()
                return lat, lng
    return None, None

def geowifi_lookup(geowifi_path, target_bssid):
    arguments = ['-s', 'bssid', target_bssid]
    try:
        print(f'[+] Running geowifi lookup for BSSID {arguments[2]}:')
        process_output = subprocess.check_output(['python', geowifi_path] + arguments, text=True)
        print(process_output)
        lat, lng = extract_lat_lon_from_output(process_output)

        if lat is not None and lng is not None:
            d = dict()
            d['lat'] = lat
            d['lng'] = lng
            return d
        else:
            print("[-] Latitude and longitude not found in the output.")
            return None

    except subprocess.CalledProcessError as e:
        print(f"[-] Error during geowifi lookup: {e}")
    except Exception as e:
        print(f"[-] An error occurred: {e}")

if __name__ == "__main__":

    # Check if the resource already exists
    if not os.path.exists(RESOURCE1_PATH):
        # If the file doesn't exist, download it
        try:
            # Create the 'recurso' directory if it doesn't exist
            os.makedirs(os.path.dirname(RESOURCE1_PATH), exist_ok=True)
            
            # Download the file
            print(f"[+] Downloading file {RESOURCE1_PATH} from {RESOURCE_URL}")
            # Download the file with tqdm for progress bar
            response = requests.get(RESOURCE_URL, stream=True)
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

    target_bssids = ["ba:46:9d:1b:28:5e", "b2:46:9d:1b:28:5e"]

    try:
        print(f"[+] Extracting file {RESOURCE1_PATH}")
        with tarfile.open(RESOURCE1_PATH, 'r:gz') as tar:
            tar.extractall(SOLVE_FILES_PATH)
        print(f'[+] Extraction of file {RESOURCE1_PATH} successful')
        print()

        print(f"[+] Extracting file {RESOURCE2_PATH}")
        with zipfile.ZipFile(RESOURCE2_PATH, 'r') as zip_ref:
            zip_ref.extractall(SOLVE_FILES_PATH)
        print(f'[+] Extraction of file {RESOURCE1_PATH} successful')
        print()

    except Exception as e:
        print(f"[-] Error during extraction: {e}")

    # Download and extract the repository
    print(f"[+] Downloading geowifi from {REPO_URL}")
    download_and_extract_github_repo(REPO_URL, SOLVE_FILES_PATH)
    print()

    try:
        # Extract all WiFi BSSIDs from the pcap file
        print(f'[+] Extracting BSSIDs from capture: {PCAP_FILE}')
        wifi_bssids = extract_wifi_bssids(PCAP_FILE)
        print()

        print(f'[+] Listing BSSIDs')
        print(wifi_bssids)
        print()

        # Find the specified BSSIDs
        found_bssids = find_specific_bssids(wifi_bssids, *target_bssids)

        if found_bssids:
            print("[+] Found the specified BSSIDs:")
            for bssid in found_bssids:
                print(f"- {bssid}")
        else:
            print("[-] No specified BSSIDs found.")

        print()

    except Exception as e:
        print(f"[-] Error: {e}")
    
    # Geowifi
    geowifi_dict = dict()

    for target_bssid in target_bssids:
        geowifi_dict[target_bssid] = geowifi_lookup(GEOWIFI_PATH, target_bssid)
        if geowifi_dict[target_bssid]:
            print(f"[+] BSSID: {target_bssid} | Latitude: {geowifi_dict[target_bssid]['lat']} | Longitude: {geowifi_dict[target_bssid]['lng']}")
            print()
    
    print("[+] Lat, Lng for BSSIDs")
    for key, value in geowifi_dict.items():
        print(f'BSSID:{key}: {value}')
        url = f'https://www.google.com/maps/place/{value["lat"]},{value["lng"]}'
        print()
        print(f'[+] Launching google maps on default web browser. URL: {url}')
        print()
        webbrowser.open(url)
    
    print()
    print(f"Get the location's name using google maps.")