# File: solve.py
# Author: Julián Casaburi
# Date: January 7, 2024
# Description: This is a script to solve the challenge "skat's SD Card (Iris CTF 2024 - Forensics)".

import subprocess
import re
import pexpect
import os

# Constants
RECURSO_DIR = './recurso'
PRIVATE_KEY_PATH = os.path.join(RECURSO_DIR, 'id_rsa')
REPO_URL = 'git@github.com:IrisSec/skats-interesting-things.git'
PASSPHRASE = "password"
SOLVE_DIR = "./solve"
REPO_DIR = os.path.join(SOLVE_DIR, "skats-interesting-things")
FLAG_DIR = os.path.join(SOLVE_DIR, "flag.txt")
COMMIT_HASH = '680ec84ca3877b9a4083242a192eb4481050edc5'

def clone_private_repo(private_key_path, passphrase, repo_url, output_dir):
    git_command = f'git'
    
    # Use pexpect to handle interactive input
    child = pexpect.spawn(git_command, ['clone', f'--config', f'core.sshCommand=ssh -i {private_key_path}', repo_url, output_dir])
    
    # Expect the passphrase prompt
    child.expect('Enter passphrase for key')
    
    # Send the passphrase
    child.sendline(passphrase)
    
    # Wait for the command to complete
    child.wait()

def find_flag_in_commit(commit_hash, repo_path):
    git_show_command = f'git -C {repo_path} show {commit_hash} | grep "irisctf{{.*}}" -oP'
    result = subprocess.run(git_show_command, shell=True, capture_output=True, text=True)
    flag_match = re.search(r'irisctf\{.*?\}', result.stdout)
    return flag_match.group() if flag_match else None

def write_flag_to_file(flag, flag_file_path):
    with open(flag_file_path, 'w') as flag_file:
        flag_file.write(flag)
    print(f"[+] Flag written to {os.path.abspath(flag_file_path)}")

def main():
    print(f'[+] Cloning private repo {REPO_URL} using key {PRIVATE_KEY_PATH} and passphrase {PASSPHRASE}')
    clone_private_repo(PRIVATE_KEY_PATH, PASSPHRASE, REPO_URL, REPO_DIR)

    print(f'[+] Searching the flag in the diff of commit {COMMIT_HASH}')
    flag = find_flag_in_commit(COMMIT_HASH, REPO_DIR)

    if flag:
        print(f'[+] Flag found in commit {COMMIT_HASH}: {flag}')

        # Create the solve directory if it doesn't exist
        os.makedirs(SOLVE_DIR, exist_ok=True)

        # Write flag to file
        write_flag_to_file(flag, FLAG_DIR)
    else:
        print('[-] Flag not found.')

if __name__ == "__main__":
    main()
