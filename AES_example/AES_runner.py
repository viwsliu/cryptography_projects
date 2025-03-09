from AES_test_v1 import AESEncryption
from AES_test_v2 import AESCipher

key = 'mysecretkey'
cipher = AESEncryption(key)
cipher2 = AESCipher(key)
# input = input("Input a message to encrypt: ")
input = "tes"

encrypted1 = cipher.encrypt(input)
print(f'Encrypted v1: {encrypted1}')

decrypted1 = cipher.decrypt(encrypted1)
print(f'Decrypted v1: {decrypted1}')


encrypted2 = cipher2.encrypt(input)
print(f'Encrypted v2: {encrypted2}')

decrypted2 = cipher2.decrypt(encrypted2)
print(f'Decrypted v2: {decrypted2}')