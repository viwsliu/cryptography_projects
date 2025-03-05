from AES_test_v1 import AESEncryption
from AES_test_v2 import AESCipher

key = 'mysecretkey'
cipher = AESCipher(key)
input = input("Input a message to encrypt: ")

encrypted = cipher.encrypt(input)
print(f'Encrypted: {encrypted}')

decrypted = cipher.decrypt(encrypted)
print(f'Decrypted: {decrypted}')
