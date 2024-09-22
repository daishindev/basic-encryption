from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import sys
from steganographyfunctions import extract_key_from_image

def ensure_extension(filename, extension):
    # adding extension check
    if filename.lower() == "exit":
        print("Exiting the program...")
        sys.exit()
    name, ext = os.path.splitext(filename)


# if the extension  missing or incorrect, append the correct one
    if ext.lower() != extension:
        return f"{name}{extension}"
    return filename

def load_key(key_file):
    with open(key_file, 'rb') as f:
        key = f.read()
    return key


def decrypt_file(input_file, output_file, stego_image_file):
    backend = default_backend()

    # extract key from image
    key_hex = extract_key_from_image(stego_image_file)
    key = bytes.fromhex(key_hex)

    # read the iv and cipher from input
    with open(input_file, 'rb') as f:
        iv = f.read(16)
        ciphertext = f.read()

    # cipher obj
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    decryptor = cipher.decryptor()

    # decrypt
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()

    # remove padding
    padding = decrypted_data[-1]
    decrypted_data = decrypted_data[:-padding]

    # write decrypted to -> file
    with open(output_file, 'wb') as f:
        f.write(decrypted_data)


# main
while True:
    try:
        file_to_decrypt = input("What file to decrypt?: ")
        file_to_decrypt = ensure_extension(file_to_decrypt, ".bin")

        if not os.path.isfile(file_to_decrypt):
            raise FileNotFoundError

        while True:
            decrypted_file_name = input("What name for the decrypted file? no spaces: ")
            decrypted_file_name = ensure_extension(decrypted_file_name, ".zip")

            stego_image_file = input("Enter the path to the image file containing the hidden key: ")

            if " " not in decrypted_file_name and os.path.isfile(stego_image_file):
                decrypt_file(file_to_decrypt, decrypted_file_name, stego_image_file)
                print(f"Decrypted file saved as: {decrypted_file_name}")
                break
            else:
                print("Invalid name or image file not found. Please try again.")

    except FileNotFoundError:
        print(f"No such file: {file_to_decrypt} - Please try again.")
        continue