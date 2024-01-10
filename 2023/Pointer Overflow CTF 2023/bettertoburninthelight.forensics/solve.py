# File: solve.py
# Author: Julián Casaburi
# Date: December 28, 2023
# Description: This is a script to solve the challenge "Better to Burn in the Light (Pointer Overflow CTF 2023 - Forensics)".

import os
import fs

def edit_jpg_file(file_path, save_path):
    try:
        # Read the contents of the file
        with open(file_path, 'rb') as file:
            data = file.read()

        # Find the second occurrence of FF D8
        start_index = data.find(b'\xFF\xD8', data.find(b'\xFF\xD8') + 1)

        if start_index != -1:
            # Delete everything before the second FF D8
            edited_data = data[start_index:]

            # Write the edited data to the new file
            with open(save_path, 'wb') as file:
                file.write(edited_data)

            print(f"[+] Editing of {file_path} and saving to {save_path} successful.")
        else:
            print("[-] JPEG marker not found in the file.")

    except Exception as e:
        print(f"[-] Error editing and saving file {file_path}: {e}")

def insert_jfif_soi(file_path, save_path):
    try:
        # Read the contents of the file
        with open(file_path, 'rb') as file:
            data = file.read()

        # JFIF SOI marker
        jfif_soi_marker = b'\xFF\xD8'

        # Insert the JFIF SOI marker at the beginning of the file
        edited_data = jfif_soi_marker + data

        # Write the edited data to the new file
        with open(save_path, 'wb') as file:
            file.write(edited_data)

        print(f"[+] Insertion of JFIF SOI marker in {file_path} and saving to {save_path} successful.")

    except Exception as e:
        print(f"[-] Error inserting JFIF SOI marker in {file_path} and saving to {save_path}: {e}")

# Config
resource_file_path = './recurso/DF3.001'
solve_folder_path = './solve'
extracted_files_folder_path = os.path.join(solve_folder_path, 'extracted-files')
fixed_files_path = os.path.join(solve_folder_path, 'fixed-files')

# Ensure the directories exists
os.makedirs(fixed_files_path, exist_ok=True)
os.makedirs(extracted_files_folder_path , exist_ok=True)

# Extract files
fat_fs = fs.open_fs(f"fat://{os.path.abspath(resource_file_path)}?read_only=true")  # Open disk image
host_fs = fs.open_fs(f"osfs://{os.path.abspath(extracted_files_folder_path)}") # Open directory on host

# Copy files from the disk image to the host_fs filesystem
fs.copy.copy_fs(fat_fs, host_fs)

print(f"[+] Extraction successful. Files extracted to {os.path.abspath(extracted_files_folder_path)}")
print()

# Fix $RECYCLE.BIN/$RN367L5.jpg within the extracted files folder (delete first JFIF header)
jpg_file_path = os.path.join(extracted_files_folder_path  , '$RECYCLE.BIN', '$RN367L5.JPG')
edited_jpg_save_path = os.path.join(fixed_files_path, 'flag_part1.jpg')

# Call the function to edit the JPG file and save it to the fixed-files directory
edit_jpg_file(jpg_file_path, edited_jpg_save_path)
print()

# Fix $RECYCLE.BIN/$R4K6JU8.doc within the extracted files folder (missing JFIF header)
doc_file_path = os.path.join(extracted_files_folder_path  , '$RECYCLE.BIN', '$R4K6JU8.DOC')
edited_doc_save_path = os.path.join(fixed_files_path, 'flag_part2.jpg')

# Call the function to insert JFIF SOI marker in the DOC file and save it to the fixed-files directory
insert_jfif_soi(doc_file_path, edited_doc_save_path)
print()

print(f'[+] Done Fixing file headers. Now open both images in {os.path.abspath(fixed_files_path)} to get the flag.')
