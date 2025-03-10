from AES_test_v1 import AESEncryption as v1
from AES_test_v2 import AESEncryption as v2

import os
import base64

key = base64.b64encode(os.urandom(16)).decode('utf-8')

cipher = v1(key)
cipher2 = v2(key)

# input = input("Input a message to encrypt: ")
input = "test"

def test_v1(input):
    encrypted = cipher.encrypt(input)
    print(f'Encrypted v1: {encrypted}, Length={len(encrypted)}')
    decrypted = cipher.decrypt(encrypted)
    print(f'Decrypted v1: {decrypted}')

def test_v2(input):
    encrypted = cipher2.encrypt(input)
    print(f'Encrypted v2: {encrypted}, Length={len(encrypted)}')
    decrypted = cipher2.decrypt(encrypted)
    print(f'Decrypted v2: {decrypted}')

print("key: ", key)
test_v1(input)
test_v2(input)
