# File: solve.py
# Author: Julián Casaburi
# Date: December 28, 2023
# Description: This is a script to solve the challenge "If You Don't, Remember Me (Pointer Overflow CTF 2023 - Forensics)".

import re
from pathlib import Path

def extract_flag(flag_with_encoded_part):
    # Split into non-hex and hex parts
    flag_beginning, flag_hex_part = flag_with_encoded_part.split('_')
    flag_beginning = flag_beginning + '_'
    flag_hex_part = flag_hex_part.strip('}')
    flag_ending = '}'

    # Decode the hex part
    decoded_hex_part = bytes.fromhex(flag_hex_part).decode('utf-8')

    # Merge parts
    flag = flag_beginning + decoded_hex_part + flag_ending

    # Replace (
    flag = flag.replace('(', '{')

    return flag

def main():
    # Regex - Pointer Overflow CTF flag format (https://pointeroverflowctf.com/rules)
    pattern = re.compile(rb'poctf.*?}', re.DOTALL)

    # Challenge resource
    pdf_file_path = Path('./recurso/DF1.pdf')
    output_file_path = Path('./solve/flag.txt')

    # Create output folder if it doesn't exist
    output_file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(pdf_file_path, 'rb') as file, open(output_file_path, 'w') as output_file:
        # Read the binary content of the PDF file
        binary_content = file.read()

        # Search for the pattern in the binary content
        match = pattern.search(binary_content)

        # Obtain the flag from the match (two-step flag partially encoded)
        if match:
            flag_with_encoded_part = match.group(0).decode("utf-8")

            # Print the original flag with encoded part
            print("[+] Flag - Step 1 (with encoded part):", flag_with_encoded_part)

            # Process the flag
            flag = extract_flag(flag_with_encoded_part)

            # Print the processed flag
            print(f'[+] Flag: {flag}')

            # Write the flag to a text file
            output_file.write(flag)
            print(f'[+] Flag written to {output_file_path.resolve()}') # Display the absolute path

        else:
            print('[-] No match found.')

if __name__ == "__main__":
    main()
