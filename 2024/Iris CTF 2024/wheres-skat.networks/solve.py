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
import json

RESOURCE_URL = "https://cdn.2024.irisc.tf/wheres-skat.tar.gz"

RESOURCE1_PATH = os.path.join(".", "recurso", "wheres-skat.tar.gz")
SOLVE_FILES_PATH = os.path.join(".", "solve")
RESOURCE2_PATH = os.path.join(SOLVE_FILES_PATH, "wheres-skat", "wheres-skat.zip")
GEOWIFI_PATH = os.path.join(SOLVE_FILES_PATH, "geowifi-main")
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

def geowifi_lookup(geowifi_path, target_bssid):
    arguments = ['-s', 'bssid', target_bssid, '-ojson']

    try:
        # Ensure geowifi_path is an absolute path
        geowifi_path = os.path.abspath(geowifi_path)
        
        print(f'[+] Running geowifi lookup for BSSID {arguments[2]}:')
        
        # Use subprocess.run to run geowifi. Change the working directory (cwd) so it can find the /results folder
        subprocess.run(['python', "geowifi.py"] + arguments, check=True, cwd=geowifi_path)

        results_path = os.path.join(geowifi_path, "results")
        print(f'[+] Geowifi lookup completed successfully. Output saved to {results_path}')

        # Get the last modified json file in geowifi_path + "/results"
        results_files = [os.path.join(results_path, f) for f in os.listdir(results_path) if os.path.isfile(os.path.join(results_path, f))]
        results_files.sort(key=lambda x: os.path.getmtime(x))
        results_file = results_files[-1]

        # Read the results_file json, extract latitude and longitude and create a dictionary
        with open(results_file, 'r') as file:
            data = json.load(file)

        # Find the "apple" module in the list
        apple_data = next((item for item in data if item.get('module') == 'apple'), None)

        if apple_data:
            # Extract latitude and longitude
            latitude = apple_data.get('latitude')
            longitude = apple_data.get('longitude')

            # Create a dictionary with latitude and longitude
            location_dict = {'latitude': latitude, 'longitude': longitude}

            return location_dict
        else:
            print("[-] No 'apple' module found in the JSON data.")
            return None
        
    except subprocess.CalledProcessError as e:
        print(f'[-] Error running geowifi: {e.stderr}')
    except Exception as e:
        print(f'[-] An unexpected error occurred: {e}')

if __name__ == "__main__":

    # Check if the resource already exists
    resource_available = True  # Track resource availability
    if not os.path.exists(RESOURCE1_PATH):
        resource_available = False
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
            
            resource_available = True
            print(f"[+] File downloaded to {RESOURCE1_PATH}")
        except Exception as e:
            print(f"[-] Failed to download the file. Error: {e}")
    else:
        print(f"[+] The file {RESOURCE1_PATH} already exists. Skipping download")

    if not resource_available:
        print(f'[-] Resource {RESOURCE1_PATH} not available. Exiting.')
        exit(1)

    target_bssids = ["ba:46:9d:1b:28:5e", "b2:46:9d:1b:28:5e"]

    try:
        print(f"[+] Extracting file {RESOURCE1_PATH} to {SOLVE_FILES_PATH}")
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
            print(f"[+] BSSID: {target_bssid} | Latitude: {geowifi_dict[target_bssid]['latitude']} | Longitude: {geowifi_dict[target_bssid]['longitude']}")
            # Save BSSID, latitude, longitude to SOLVE_FILES_PATH + target_bssid (replace : with _) + ".txt"
            bssid_flag_path = os.path.join(SOLVE_FILES_PATH, target_bssid.replace(':', '_') + ".txt")
            with open(bssid_flag_path, 'w') as file:
                file.write(f'BSSID: {target_bssid}\n')
                file.write(f'Latitude: {geowifi_dict[target_bssid]["latitude"]}\n')
                file.write(f'Longitude: {geowifi_dict[target_bssid]["longitude"]}\n')
                print(f"[+] {target_bssid} coords written to {os.path.abspath(bssid_flag_path)}")
            print()
    
    print("[+] Lat, Lng for BSSIDs")
    for key, value in geowifi_dict.items():
        print(f'BSSID:{key}: {value}')
        url = f'https://www.google.com/maps/place/{value["latitude"]},{value["longitude"]}'
        print()
        print(f'[+] Launching google maps on default web browser. URL: {url}')
        print()
        webbrowser.open(url)
    
    print()
    print(f"[+] FLAG: Get the location's name using google maps. Format: 'irisctf{{location_name}}'")