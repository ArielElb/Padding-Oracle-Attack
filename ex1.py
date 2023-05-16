from Cryptodome.Cipher import DES
from Cryptodome.Util.Padding import unpad
import sys

def xor(a, b, c):
    return bytes([a ^ b ^ c])

def oracle(ciphertext, key, iv):
    try:
        cipher = DES.new(key, DES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext), 8)
        return True
    except ValueError:
        return False

def decrypt(ciphertext, key, iv):
    cipher = DES.new(key, DES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), 8)
    return plaintext

def attack_per_block(blockBefore, blockToDecrypt, isLastBlock):
    c = bytes([0] * 8) + blockToDecrypt
    realText = [0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(8):
        while True:
            for j in range(256):
                if oracle(c, key, iv):
                    break
                c = c[:7 - i] + bytes([c[7 - i] + 1]) + c[8 - i:]
            break

        # i+1 is the byte we forcing to be (P'j[x] ^ c[7-i]) is the byte after decryption but not yet xored with the previous block byte
        # than we xor it with the previous block byte to get the real value of the byte in the plaintext
        #
        last = xor(i + 1, blockBefore[(7 - i)], c[7 - i])
        realText[7 - i] = last

        for k in range(i + 1):
            # var is the updated value in the test block
            # we need to update all the Xk[x] bytes in the test block
            # than we getting the values for the next iteration
            var = xor(i + 2, blockBefore[(7 - k)], int(realText[7 - k].hex(), 16))
            c = c[:7 - k] + var + c[8 - k:]

    result = ''
    for item in realText:
        result += item.hex()

    if isLastBlock:
        return unpad(bytes.fromhex(result), 8).decode()
    else:
        byte_data = bytes.fromhex(result)
        return byte_data.decode()


# decrypt the first block
def attack_first_block(blockToDecrypt):
    c = bytes([0] * 8) + blockToDecrypt
    realText = [0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(8):
        while True:
            for j in range(256):
                if oracle(c, key, iv):
                    break
                c = c[:7 - i] + bytes([c[7 - i] + 1]) + c[8 - i:]
            break

        # i+1 is the byte we forcing to be (P'j[x] ^ c[7-i]) is the byte after decryption but not yet xored with
        # the previous block byte
        # than we xor it with the previous block byte to get the real value of the byte in the plaintext
        last = xor(i + 1, iv[7 - i], c[7 - i])
        realText[7 - i] = last

        for k in range(i + 1):
            # var is the updated value in the test block
            # we need to update all the Xk[x] bytes in the test block
            # than we getting the values for the next iteration
            var = xor(i + 2, iv[7 - i], int(realText[7 - k].hex(), 16))
            c = c[:7 - k] + var + c[8 - k:]

    result = ''
    for item in realText:
        result += item.hex()

    byte_data = bytes.fromhex(result)
    return byte_data.decode()


ciphertext = bytes.fromhex(sys.argv[1])
key = bytes.fromhex(sys.argv[2])
iv = bytes.fromhex(sys.argv[3])
dycryptedText = ''
for i in range(0, len(ciphertext), 8):
    if i == 0:
        dycryptedText += attack_first_block(ciphertext[:8])
    else:
        dycryptedText += attack_per_block(ciphertext[i - 8:i], ciphertext[i:i + 8], i == len(ciphertext) - 8)

print(dycryptedText)