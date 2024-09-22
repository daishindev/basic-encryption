import numpy as np
from PIL import Image


def int_to_bin(num):
    return format(num, '08b')


def bin_to_int(binary):
    return int(binary, 2)


def hide_key_in_image(key, image_path, output_path):
    # Open the image
    img = Image.open(image_path)
    width, height = img.size
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4

    total_pixels = array.size // n

    # Convert key to binary
    binary_key = ''.join([int_to_bin(ord(char)) for char in key])
    key_length = len(binary_key)

    if key_length > total_pixels:
        raise ValueError("Key is too large for the image")

    # Embed the key length (32 bits) at the beginning
    length_binary = format(key_length, '032b')

    index = 0
    for i in range(32):
        array[index][0] = (array[index][0] & 254) | int(length_binary[i])
        index += 1

    # Embed the key
    for i in range(key_length):
        array[index][0] = (array[index][0] & 254) | int(binary_key[i])
        index += 1

    # Save the image
    array = array.reshape(height, width, n)
    result = Image.fromarray(array.astype('uint8'), img.mode)
    result.save(output_path)


def extract_key_from_image(image_path):
    # Open the image
    img = Image.open(image_path)
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4

    # Extract the key length
    length_binary = ''.join([str(array[i][0] & 1) for i in range(32)])
    key_length = int(length_binary, 2)

    # Extract the key
    binary_key = ''.join([str(array[i][0] & 1) for i in range(32, 32 + key_length)])

    # Convert binary key to string
    key = ''.join([chr(bin_to_int(binary_key[i:i + 8])) for i in range(0, len(binary_key), 8)])

    return key