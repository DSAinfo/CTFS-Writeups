# File: solve.py
# Author: Julián Casaburi
# Date: January 6, 2024
# Description: This is a script to solve the challenge "Czech Where? (Iris CTF 2024 - Open-Source Intelligence)".

import requests
import re
import unicodedata
import os

SOLVE_FILES_PATH = "./solve"
FLAG_FILE_PATH = os.path.join(SOLVE_FILES_PATH, "flag.txt")
GOOGLE_MAPS_URL = "https://www.google.com/maps/search/"

def write_flag_to_file(flag, flag_file_path):
    with open(flag_file_path, 'w') as flag_file:
        flag_file.write(flag)
    print(f"[+] Flag written to {os.path.abspath(flag_file_path)}")

def is_valid_street_name(candidate):
    return candidate != "null" and all(char.isalpha() or char.isspace() for char in candidate) and len(candidate) > 1

def extract_all_location_info(script_content, place_name):
    unique_locations = set()
    start_index = 0

    while True:
        index = script_content.find(place_name, start_index)
        if index == -1:
            break

        first_comma_index = script_content.find(',', index)
        second_comma_index = script_content.find(',', first_comma_index + 1)

        if first_comma_index != -1 and second_comma_index != -1:
            result_string = script_content[first_comma_index + 1:second_comma_index].strip()
            if is_valid_street_name(result_string) and result_string not in unique_locations:
                yield result_string
                unique_locations.add(result_string)

        start_index = index + 1

def create_flags(location_names):
    return ['irisctf{{{}}}'.format(''.join(c for c in unicodedata.normalize('NFD', loc.lower()) if unicodedata.category(c) != 'Mn')) for loc in location_names]

def print_possible_flags(flags):
    print(f'[+] Possible Flags ({len(flags)}):')
    for flag in flags:
        flag = flag.replace(" ", "_")
        print(f'  - {flag}')

def process_location_info(place_name, response_text):
    location_names = list(extract_all_location_info(response_text, place_name))

    if location_names:
        print(f'[+] Possible Street Names ({len(location_names)}):')
        for location_name in location_names:
            print(f"  - {location_name}")
        
        print()

        flags = create_flags(location_names)
        print_possible_flags(flags)

        print()

        if not os.path.exists(SOLVE_FILES_PATH):
            os.makedirs(SOLVE_FILES_PATH)

        for i, flag in enumerate(flags):
            flag_file_path = os.path.join(SOLVE_FILES_PATH, f"flag_{i + 1}.txt")
            write_flag_to_file(flag, flag_file_path)

        return location_names
    else:
        print("[-] No location information found.")
        return None

def get_all_location_info(place_name):
    formatted_place_name = re.sub(r'\s+', '+', place_name)
    url = f"{GOOGLE_MAPS_URL}{formatted_place_name}"

    try:
        print(f'[+] Requesting Google Maps... {url}')
        response = requests.get(url)

        if response.status_code == 200:
            print()
            return process_location_info(place_name, response.text)
        else:
            print(f"[-] Error: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"[-] Error: {e}")
        return None

def main():
    place_name = "Czech Wooden Products"
    location_names = get_all_location_info(place_name)

if __name__ == "__main__":
    main()
