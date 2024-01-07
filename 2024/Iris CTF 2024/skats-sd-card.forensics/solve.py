# File: solve.py
# Author: Julián Casaburi
# Date: January 7, 2024
# Description: This is a script to solve the challenge "skat's SD Card (Iris CTF 2024 - Forensics)".

import subprocess
import re
import pexpect
import os

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
    print(f'[+] Flag written to {flag_file_path}')

def main():
    # Cloning private repo
    private_key_path = './recurso/id_rsa'
    repo_url = 'git@github.com:IrisSec/skats-interesting-things.git'
    output_dir = './solve/skats-interesting-things'
    passphrase = "password"
    print(f'[+] Cloning private repo {repo_url} using key {private_key_path} and passphrase {passphrase}')
    clone_private_repo(private_key_path, passphrase, repo_url, output_dir)

    # Finding flag in commit
    commit_hash = '680ec84ca3877b9a4083242a192eb4481050edc5'
    print(f'[+] Searching the flag in the diff of commit {commit_hash}')
    flag = find_flag_in_commit(commit_hash, output_dir)

    if flag:
        print(f'[+] Flag found in commit {commit_hash}: {flag}')

        SOLVE_FILES_PATH = "./solve"

        # Write flag to file
        # Create the solve directory if it doesn't exist
        if not os.path.exists(SOLVE_FILES_PATH):
            os.makedirs(SOLVE_FILES_PATH)

        write_flag_to_file(flag, SOLVE_FILES_PATH + "/flag.txt")
    else:
        print('[-] Flag not found.')

if __name__ == "__main__":
    main()
