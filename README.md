# basic-steganographic-encryption
This project implements a file encryption system that uses steganography to hide encryption keys within images. It provides a secure way to encrypt files and share them, with the decryption key hidden in plain sight. Note that this encryption is not secure for complex stuff. I did this project just so I can encrypt files in a very basic way and give the key to whomever I need to.
Features

## Features

- File encryption using AES-256 in CBC mode
- Steganographic hiding of encryption keys in images
- File decryption using keys extracted from images
- Command-line interface for easy use

## Requirements

- Python 3.6+
- cryptography
- numpy
- Pillow (PIL)

## Installation

Install the required packages:
   ```
   pip install cryptography numpy pillow
   ```

## Usage
As i mentioned before, this is a very basic encryption, it isnt supposed to be super serious.
### Encryption
Run the `encryption.py` script and follow the prompts:

```
python encryption.py
```

You will be asked for:
1. The file you want to encrypt
2. A name for the encrypted file (will be saved with .bin extension)
3. An image file to hide the encryption key in

The script will create an encrypted .bin file and a new image file with the hidden key.

### Decryption

Run the `decrypt.py` script and follow the prompts:

```
python decrypt.py
```

You will be asked for:
1. The .bin file you want to decrypt
2. A name for the decrypted file
3. The image file containing the hidden key

The script will extract the key from the image, decrypt the file, and save it with the specified name.

## How it Works

1. **Encryption**: 
   - Generates a random 256-bit key
   - Encrypts the file using AES-256 in CBC mode
   - Hides the key in the least significant bits of the pixels in the provided image

2. **Decryption**:
   - Extracts the key from the image
   - Uses the key to decrypt the file

3. **Steganography**:
   - The `stenographyfunctions.py` file contains functions to hide and extract data in images
   - It uses the least significant bit of the red channel of each pixel to store data

## Security Considerations

- The security of this system relies on keeping the image with the hidden key secret
- If an attacker obtains both the encrypted file and the image, they can potentially decrypt the file
- Always use secure methods to transfer the image file

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
