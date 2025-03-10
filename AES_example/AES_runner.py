from AES_test_v1 import AESEncryption
from AES_test_v2 import AESCipher
from AES_test_v3 import AESEncryption
import os
import base64

key = base64.b64encode(os.urandom(16)).decode('utf-8')

cipher = AESEncryption(key)
cipher2 = AESCipher(key)
cipher3 = AESEncryption(key)

# input = input("Input a message to encrypt: ")
input = "test"

def test_v1(input):
    encrypted = cipher.encrypt(input)
    print(f'Encrypted v1: {encrypted}')
    decrypted = cipher.decrypt(encrypted)
    print(f'Decrypted v1: {decrypted}')

def test_v2(input):
    encrypted = cipher2.encrypt(input)
    print(f'Encrypted v2: {encrypted}')
    decrypted = cipher2.decrypt(encrypted)
    print(f'Decrypted v2: {decrypted}')

def test_v3(input):
    encrypted = cipher3.encrypt(input)
    print(f'Encrypted v3: {encrypted}')
    decrypted = cipher3.decrypt(encrypted)
    print(f'Decrypted v3: {decrypted}')

print("key: ", key)
test_v1(input)
test_v2(input)
test_v3(input)