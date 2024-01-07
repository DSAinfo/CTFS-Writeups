# File: solve.py
# Author: Julián Casaburi
# Date: January 6, 2024
# Description: This is a script to solve the challenge "Czech Where? (Iris CTF 2024 - Open-Source Intelligence)".

import requests
import re
import unicodedata
import os

SOLVE_FILES_PATH = "./solve"

def write_flag_to_file(flag, flag_file_path):
    with open(flag_file_path, 'w') as flag_file:
        flag_file.write(flag)
    print(f'[+] Flag written to {flag_file_path}')

def extract_location_info(html_content, place_name):
    # Extract content between script tags
    script_content = re.search(r'<script nonce="[^"]+">(.*?)</script>', html_content, re.DOTALL)

    if script_content:
        script_content = script_content.group(1)

        occurrence_count = 0
        start_index = 0

        while occurrence_count < 6:
            index = script_content.find(place_name, start_index)
            if index == -1:
                break
            occurrence_count += 1
            start_index = index + 1

        if index != -1:
            # Find the positions of the first and second commas
            first_comma_index = script_content.find(',', index)
            second_comma_index = script_content.find(',', first_comma_index + 1)

            if first_comma_index != -1 and second_comma_index != -1:
                result_string = script_content[first_comma_index + 1:second_comma_index].strip()
                return result_string

    return None

def get_location_info(place_name):
    base_url = "https://www.google.com/maps/search/"
    formatted_place_name = re.sub(r'\s+', '+', place_name)

    url = f"{base_url}{formatted_place_name}"
    response = requests.get(url)

    if response.status_code == 200:
        location_name = extract_location_info(response.text, place_name)

        if location_name:
            print(f"[+] Location Name: {location_name}")
            # Convert to lowercase
            location_name = location_name.lower()

            # Replace whitespace with underscores
            location_name = location_name.replace(" ", "_")

            # Remove accent marks
            flag = ''.join(c for c in unicodedata.normalize('NFD', location_name) if unicodedata.category(c) != 'Mn')
            flag = "irisctf{{{}}}".format(flag)

            # Print flag
            print(f'[+] Flag: {flag}')

            # Write flag to file
            # Create the solve directory if it doesn't exist
            if not os.path.exists(SOLVE_FILES_PATH):
                os.makedirs(SOLVE_FILES_PATH)

            write_flag_to_file(flag, SOLVE_FILES_PATH + "/flag.txt")
            
            return location_name
        else:
            print("[-] No location information found.")
            return None
    else:
        print(f"[-] Error: {response.status_code}")
        return None

place_name = "Czech Wooden Products"
location_name = get_location_info(place_name)
