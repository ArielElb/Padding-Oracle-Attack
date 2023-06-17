# Padding-Oracle-Attack

![image](https://github.com/ArielElb/Padding-Oracle-Attack/assets/94087682/a3efbdb5-099d-4d04-ac0f-7d0da6320811)

This repository contains a Python implementation of a padding oracle attack on a block cipher using the DES encryption algorithm. The attack aims to decrypt a given ciphertext by exploiting a vulnerability in the padding scheme used.

## Prerequisites

To run the code, you need to have the following:

- Python 3.x
- `pycryptodome` library (`pip install pycryptodome`)

## Usage

1. Clone the repository:

2. Navigate to the project directory: cd padding-oracle-attack

3. Run the attack script: python3 attack.py <ciphertext> <key> <iv>

Make sure to replace `<ciphertext>`, `<key>`, and `<iv>` with the appropriate values. The `<ciphertext>` should be provided as a hexadecimal string, while the `<key>` and `<iv>` should be provided as plain text.

4. The decrypted plaintext will be displayed in the console output.

## Explanation

The padding oracle attack exploits a vulnerability in the padding scheme used in the DES block cipher. The attack works by iteratively modifying the ciphertext and utilizing the padding oracle function to retrieve the decrypted blocks.

The code consists of the following components:

- `oracle`: This function acts as the padding oracle. It attempts to decrypt the ciphertext using the provided key and IV, and checks if the padding is correct. It returns `True` if the padding is correct, and `False` otherwise.

- `decrypt`: This function decrypts a given ciphertext using the DES cipher in CBC mode and removes the padding to obtain the plaintext.

- `attack_per_block`: This function performs the attack on a single block. It iteratively modifies the ciphertext and exploits the padding oracle to retrieve the decrypted block.

The main function reads the command-line arguments (`<ciphertext>`, `<key>`, and `<iv>`) and calls the `attack_per_block` function for each block in the ciphertext. The decrypted blocks are concatenated and displayed as the resulting plaintext.

Please note that this code assumes the use of the DES cipher, which is considered outdated and insecure for many applications. Additionally, the padding oracle vulnerability exploited here is generally not present in properly implemented and secure cryptographic systems.

## License

This project is licensed under the [MIT License](LICENSE).

Feel free to explore, modify, and use the code according to the terms of the license.
