#Vincent Liu
# I decided to use the "cryptography" python library
# https://cryptography.io/en/latest/

from cryptography.hazmat.primitives.ciphers import Cipher, modes, algorithms
# https://cryptography.io/en/latest/hazmat/primitives/symmetric-encryption/#cryptography.hazmat.primitives.ciphers.Cipher
# https://cryptography.io/en/latest/hazmat/primitives/symmetric-encryption/#algorithms
# https://cryptography.io/en/latest/hazmat/primitives/symmetric-encryption/#module-cryptography.hazmat.primitives.ciphers.modes

from cryptography.hazmat.primitives import hashes
# https://cryptography.io/en/latest/hazmat/primitives/cryptographic-hashes/#cryptography.hazmat.primitives.hashes.Hash

from cryptography.hazmat.backends import default_backend
#provides access to the underlying implementation of algorithms and operations such as encryption, decryption, and hashing 

import base64 # used to encode/decode binary data to/from ASCII text
import os

class AESEncryption(object):
    def __init__(self, key):
        self.key = self._hash_key(key)
        self.iv = os.urandom(16)  # random 16-byte IV
        #since we will use a 128 byte key, we will perform 10 rounds of encryption (AES128)

    def _hash_key(self, key): #takes a 128 bit key and produces a hashed output using SHA-256
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(key.encode('utf-8')) #converts input key to bytes using UTF-8 endcoding, since hash functions work on byte data
        return digest.finalize()[:16] #only return the first 16 bytes (128 bits of the hash)

    def _pad(self, encoded_plaintext): #implements PKS-57 padding. used when plaintext is not a multiple of 16 bytes
        block_size = 16 #standard block size of AES
        pad_len = block_size - len(encoded_plaintext) % block_size #calculate how many bytes are needed to reach the next multiple of 16
        padding = bytes([pad_len]) * pad_len
        return encoded_plaintext + padding 

    def _unpad(self, decrypted_padded): #removes padding from ciphertext when decrypting
        pad_len = decrypted_padded[-1]
        return decrypted_padded[:-pad_len]

    def encrypt(self, plaintext):
        padded_plaintext = self._pad(plaintext.encode('utf-8')) #apply padding
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv), backend=default_backend()) #initialize AES cipher in CBC mode
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize() #encrypt
        return base64.b64encode(self.iv + ciphertext) #prepend the IV to the ciphertext and encode to base64

    def decrypt(self, ciphertext): 
        ciphertext = base64.b64decode(ciphertext) # decode base64 and separate the IV from the ciphertext
        iv = ciphertext[:16]  # extract the IV (first 16 bytes)
        actual_ciphertext = ciphertext[16:] #get the encrypted data
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend()) #initialize AES cipher in CBC mode
        decryptor = cipher.decryptor()
        decrypted_padded = decryptor.update(actual_ciphertext) + decryptor.finalize() # Decrypt and remove padding
        plaintext = self._unpad(decrypted_padded)
        return plaintext.decode('utf-8')

if __name__ == "__main__":
    input_plaintext_file = 'plaintext.txt'
    input_key_file = 'key.txt' 
    
    with open(input_plaintext_file, 'r') as file:
        input_data = file.read()

    with open(input_key_file, 'r') as file:
        key = file.read()

    test = AESEncryption(key)
    encrypted = test.encrypt(input_data)
    print(f'Encrypted v2: {encrypted} \n')

    decrypted = test.decrypt(encrypted)
    print(f'Decrypted v2: {decrypted}')