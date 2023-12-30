# File: solve.py
# Author: Julián Casaburi
# Date: December 28, 2023
# Description: This is a script to solve the challenge "The Gentle Rocking of the Sun (Pointer Overflow CTF 2023 - Cracking)".

import hashlib
import subprocess
import os
import re
import urllib.request
import py7zr

HASH = "4bd939ed2e01ed1e8540ed137763d73cd8590323"
RESOURCE_PATH = "./recurso/crack2.7z"
WORDLIST_PATH = "./german_de_DE.dic"
SOLVE_FILES_PATH = "./solve"
PASSWORD_FILE_PATH = SOLVE_FILES_PATH + "/password_7z_step1.txt"
FLAG_FILE_PATH = SOLVE_FILES_PATH + "/flag.txt"


def detect_hash_type(hash_value):
    hash_algorithms = {
        32: hashlib.md5,
        40: hashlib.sha1,
        64: hashlib.sha256,
        128: hashlib.sha512,
    }

    hash_length = len(hash_value)
    return hash_algorithms.get(hash_length, None)


def concatenate_subdirectories(directory_path):
    # Check if the provided path is a directory
    if not os.path.isdir(directory_path):
        print(f"[-] The specified path '{directory_path}' is not a directory.")
        return

    # Initialize an empty list to store all subdirectory names
    all_subdirectories = []

    # Walk through the directory and its subdirectories
    for root, dirs, files in os.walk(directory_path):
        # Add the names of subdirectories to the list
        all_subdirectories.extend(dirs)

    # Concatenate subdirectory names into a string
    result_string = "".join(all_subdirectories)

    return result_string


def main():
    try:
        hash_algorithm = detect_hash_type(HASH)
        if hash_algorithm is None:
            print(f"[-] Error: Unknown hash type for hash {HASH}")
            exit()

        # Download the dictionary if not present
        if not os.path.isfile(WORDLIST_PATH):
            print(
                f"[+] Downloading the German dictionary to {os.path.abspath(WORDLIST_PATH)}"
            )
            dictionary_url = "https://github.com/CSL-LABS/CrackingWordLists/raw/master/dics/lang/german_de_DE.dic"
            with urllib.request.urlopen(dictionary_url) as response:
                with open(WORDLIST_PATH, "wb") as wordlist_file:
                    wordlist_file.write(response.read())

        with open(
            WORDLIST_PATH, "r", encoding="utf-8", errors="ignore"
        ) as wordlist_file:
            for word in map(str.strip, wordlist_file):
                guess = hash_algorithm(word.encode("utf-8")).hexdigest()
                if guess.lower() == HASH or guess.upper() == HASH:
                    print()
                    print("[+] Hashing algorithm:", hash_algorithm.__name__)
                    print(f"[+] Password found: {word}")

                    # Create the solve directory if it doesn't exist
                    if not os.path.exists(SOLVE_FILES_PATH):
                        os.makedirs(SOLVE_FILES_PATH)

                    # Write the password to a file
                    with open(PASSWORD_FILE_PATH, "w", encoding="utf-8") as flag_file:
                        flag_file.write(word)
                        print(
                            f"[+] 7z file password written to {os.path.abspath(PASSWORD_FILE_PATH)}"
                        )
                    print()

                    # Extract the challenge resource
                    try:
                        print(f"[+] Extracting file", RESOURCE_PATH)
                        with py7zr.SevenZipFile(RESOURCE_PATH, mode='r', password=word) as z:
                            z.extractall(SOLVE_FILES_PATH)
                        print("[+] Extraction successful")
                        print()

                        # Get the flag
                        concatenated_string = concatenate_subdirectories(
                            SOLVE_FILES_PATH
                        )

                        pattern = re.compile(r"poctf.*?}", re.DOTALL)
                        matches = pattern.findall(concatenated_string)

                        for match in matches:
                            flag_content = match
                            print(f"[+] Flag: {flag_content}")

                            with open(
                                FLAG_FILE_PATH, "w", encoding="utf-8"
                            ) as flag_file:
                                flag_file.write(flag_content)
                                print(
                                    f"[+] Flag written to {os.path.abspath(FLAG_FILE_PATH)}"
                                )

                    except Exception as e:
                        print(f"[-] Error during extraction: {e}")
                    exit(0)
                else:
                    print(f"[-] Trying: {word} incorrect... {guess}")

        print(f"[-] Password not found in wordlist...")
    except FileNotFoundError:
        print(f"[-] Error: Wordlist not found at {WORDLIST_PATH}")


if __name__ == "__main__":
    main()
