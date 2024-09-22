import os
import sys
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from steganographyfunctions import hide_key_in_image

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

def save_key(key, key_file):
    # save the encryption key to a file
    with open(key_file, 'wb') as f:
        f.write(key)


def encrypt_file(input_file, output_file, stego_image_file):
    backend = default_backend()

    # generate 256 bit key
    key = os.urandom(32)

    # hide key in image
    hide_key_in_image(key.hex(), stego_image_file, f"{stego_image_file}.png")

    # iv generation
    iv = os.urandom(16)

    # create cipher obj
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)

    encryptor = cipher.encryptor()

    # read input file
    with open(input_file, 'rb') as f:
        plaintext = f.read()

    # padding for aes
    padding = 16 - len(plaintext) % 16
    plaintext += bytes([padding]) * padding

    # encrypt
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    # write iv and ciphertext to -> file
    with open(output_file, 'wb') as f:
        f.write(iv + ciphertext)


# main
while True:
    try:
        file_to_encrypt = input("What file to encrypt?: ")
        if file_to_encrypt.lower() == "exit":
            print("Exiting the program...")
            sys.exit()
        if not os.path.isfile(file_to_encrypt):
            raise FileNotFoundError

        while True:
            encrypted_file_name = input("What to name your encrypted file?: ")
            encrypted_file_name = ensure_extension(encrypted_file_name, ".bin")

            stego_image_file = input("Enter the path to the image file for hiding the key: ")

            if " " not in encrypted_file_name and os.path.isfile(stego_image_file):
                encrypt_file(file_to_encrypt, encrypted_file_name, stego_image_file)
                print(f"Encrypted file saved as: {encrypted_file_name}")
                print(f"Key hidden in image: {stego_image_file}.png")
                break
            else:
                print("Invalid name or image file not found. Please try again.")

    except FileNotFoundError:
        print(f"No such file: {file_to_encrypt} - Please try again.")
        continue
