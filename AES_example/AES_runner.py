from AES_test_v1 import AESEncryption as v1
from AES_test_v2 import AESEncryption as v2

key_file = 'key.txt'
input_file = 'plaintext.txt'
cipher_file = 'ciphertext.txt'
decrypted_file_v1 = 'decrypted_v1.txt'
decrypted_file_v2 = 'decrypted_v2.txt'

# read key from key.txt
with open(key_file, 'r') as file:
    try:
        key = file.read()
    except:
        print("key.txt DOES NOT EXIST")

# Read the plaintext input
with open(input_file, 'r') as file:
    try:
        plaintext = file.read()
    except:
        print("plaintext.txt DOES NOT EXIST")

AES_v1 = v1(key)
AES_v2 = v2(key)

def test_v1(data):
    encrypted = AES_v1.encrypt(data)
    decrypted = AES_v1.decrypt(encrypted)

    print(f'Encrypted v1: {encrypted}\n')
    print(f'Decrypted v1: {decrypted}\n')

    return encrypted, decrypted

def test_v2(data):
    encrypted = AES_v2.encrypt(data)
    decrypted = AES_v2.decrypt(encrypted)

    print(f'Encrypted v2: {encrypted}\n')
    print(f'Decrypted v2: {decrypted}\n')

    return encrypted, decrypted

# Test both encryption versions
encrypted_v1, decrypted_v1= test_v1(plaintext)
encrypted_v2, decrypted_v2 = test_v2(plaintext)

# Write encrypted outputs to the output file
with open(cipher_file, 'w') as file:
    file.write(f'Encrypted v1: {encrypted_v1}\n')
    file.write(f'Encrypted v2: {encrypted_v2}\n')

# write decrypted output to respective output files
with open(decrypted_file_v1, 'w') as file:
    file.write(decrypted_v1)

with open(decrypted_file_v2, 'w') as file:
    file.write(decrypted_v2)