import hashlib
import os
import re
import urllib.request
import py7zr
from tqdm import tqdm

# Constants
HASH = "4bd939ed2e01ed1e8540ed137763d73cd8590323"
RESOURCE_PATH = "./recurso/crack2.7z"
WORDLIST_PATH = "./german_de_DE.dic"
SOLVE_FILES_PATH = "./solve"
PASSWORD_FILE_PATH = os.path.join(SOLVE_FILES_PATH, "password_7z_step1.txt")
FLAG_FILE_PATH = os.path.join(SOLVE_FILES_PATH, "flag.txt")

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
    if not os.path.isdir(directory_path):
        print(f"[-] The specified path '{directory_path}' is not a directory.")
        return None
    all_subdirectories = []
    for root, dirs, files in os.walk(directory_path):
        all_subdirectories.extend(dirs)
    return "".join(all_subdirectories)

def download_dictionary(url, destination_path):
    print(f"[+] Downloading dictionary to {os.path.abspath(destination_path)}")
    with urllib.request.urlopen(url) as response:
        total_size = int(response.info().get('Content-Length', 0))
        block_size = 1024  # 1 Kibibyte
        with tqdm(total=total_size, unit='B', unit_scale=True) as progress_bar:
            with open(destination_path, 'wb') as wordlist_file:
                while True:
                    data = response.read(block_size)
                    if not data:
                        break
                    wordlist_file.write(data)
                    progress_bar.update(len(data))

def count_passwords(wordlist_path):
    return sum(1 for _ in open(wordlist_path, "r", encoding="utf-8", errors="ignore"))

def main():
    try:
        hash_algorithm = detect_hash_type(HASH)
        if hash_algorithm is None:
            print(f"[-] Unknown hash type for hash {HASH}")
            exit()

        print(f"[+] Hashing algorithm: {hash_algorithm.__name__}")
        print("")

        # Check if the dictionary file already exists
        if os.path.isfile(WORDLIST_PATH):
            print(f"[-] Dictionary found at {os.path.abspath(WORDLIST_PATH)}. Skipping download.")
        else:
            # Download the dictionary if not present
            download_dictionary("https://github.com/CSL-LABS/CrackingWordLists/raw/master/dics/lang/german_de_DE.dic", WORDLIST_PATH)

        total_passwords = count_passwords(WORDLIST_PATH)

        with open(WORDLIST_PATH, "r", encoding="utf-8", errors="ignore") as wordlist_file:
            progress_bar = tqdm(wordlist_file, total=total_passwords, desc='[/] Progress (pw/hash comparison)', unit="word")
            for word in progress_bar:
                guess = hash_algorithm(word.strip().encode("utf-8")).hexdigest()
                if guess.lower() == HASH or guess.upper() == HASH:
                    progress_bar.close()
                    print(f"[+] Password found: {word.strip()}")
                    if not os.path.exists(SOLVE_FILES_PATH):
                        os.makedirs(SOLVE_FILES_PATH)

                    with open(PASSWORD_FILE_PATH, "w", encoding="utf-8") as flag_file:
                        flag_file.write(word.strip())
                        print(f"[+] 7z file password written to {os.path.abspath(PASSWORD_FILE_PATH)}")
                    print("")

                    try:
                        print(f"[+] Extracting file {RESOURCE_PATH}")
                        with py7zr.SevenZipFile(RESOURCE_PATH, mode='r', password=word.strip()) as z:
                            z.extractall(SOLVE_FILES_PATH)
                        print("[+] Extraction successful")
                        print()

                        concatenated_string = concatenate_subdirectories(SOLVE_FILES_PATH)

                        pattern = re.compile(r"poctf.*?}", re.DOTALL)
                        matches = pattern.findall(concatenated_string)

                        for match in matches:
                            flag_content = match
                            print(f"[+] Flag: {flag_content}")

                            with open(FLAG_FILE_PATH, "w", encoding="utf-8") as flag_file:
                                flag_file.write(flag_content)
                                print(f"[+] Flag written to {os.path.abspath(FLAG_FILE_PATH)}")

                    except Exception as e:
                        print(f"[-] Error during extraction: {e}")

                    finally:
                        exit(0)

        print("[-] Password not found in wordlist...")

    except FileNotFoundError:
        print(f"[-] Wordlist not found at {WORDLIST_PATH}")

if __name__ == "__main__":
    main()
