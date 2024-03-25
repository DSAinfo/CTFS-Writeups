# File: solve.py
# Author: Julián Casaburi
# Date: December 28, 2023
# Description: This is a script to solve the first step of the challenge "A Petty Wage in Regret (Pointer Overflow CTF 2023 - Forensics)".

from PIL import Image
import os

SOLVE_FILES_PATH = "./solve"
FLAG_PART1_FILE_PATH = os.path.join(SOLVE_FILES_PATH, "flag_part1.txt")

def get_decoded_user_comment(img):
    exif_data = img._getexif()

    if exif_data and 37510 in exif_data:  # Check if UserComment tag exists
        user_comment = exif_data[37510]  # UserComment tag
        user_comment = user_comment.strip(b'ASCII').strip(b'\x00')
        user_comment = user_comment.decode('utf-8')
        user_comment = bytes.fromhex(user_comment).decode('utf-8')
        return user_comment
    else:
        return None

def main():
    image_path = './recurso/DF2.jpg'

    with Image.open(image_path) as img:
        user_comment = get_decoded_user_comment(img)

        if user_comment:
            print("[+] Decoded hex EXIF User Comment:", user_comment)

            # Extract the part of user_comment that starts with "poctf{"
            flag_start_index = user_comment.find("poctf{")
            if flag_start_index != -1:
                extracted_flag = user_comment[flag_start_index:]
                print("[+] Flag P1/2:", extracted_flag)
                
                # Create the solve directory if it doesn't exist
                os.makedirs(SOLVE_FILES_PATH, exist_ok=True)
                
                # Save the result to step1.txt
                with open(FLAG_PART1_FILE_PATH, 'w') as step1_file:
                    step1_file.write("[+] Decoded hex EXIF User Comment: {}\n".format(user_comment))
                    step1_file.write("[+] Flag P1/2: {}\n".format(extracted_flag))
                
                print(f"[+] Flag P1/2 written to {os.path.abspath(FLAG_PART1_FILE_PATH)}")

                print(f"[+] Opening challenge image in the OS default image viewer")
                img.show()  # Open img in the user's default image viewer
            else:
                print("[-] No 'poctf{' found in the User Comment.")
        else:
            print("[-] No User Comment found in the EXIF data.")

if __name__ == "__main__":
    main()
