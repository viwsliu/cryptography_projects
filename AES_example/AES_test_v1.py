from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
#for documentation on each of the imports in order:
# https://cryptography.io/en/latest/hazmat/primitives/symmetric-encryption/#cryptography.hazmat.primitives.ciphers.Cipher
# https://cryptography.io/en/latest/hazmat/primitives/symmetric-encryption/#algorithms
# https://cryptography.io/en/latest/hazmat/primitives/symmetric-encryption/#module-cryptography.hazmat.primitives.ciphers.modes

from cryptography.hazmat.primitives import hashes
#for documentation on import:
# https://cryptography.io/en/latest/hazmat/primitives/cryptographic-hashes/#cryptography.hazmat.primitives.hashes.Hash

from cryptography.hazmat.backends import default_backend
# Provides access to the underlying implementation of algorithms and operations such as encryption, decryption, and hashing 

import base64 # used to encode/decode binary data to/from ASCII text
import os #used to generate random data for the Init Vector


class AESEncryption(object):
    def __init__(self, key):
        self.key = self._hash_key(key)
        self.iv = os.urandom(16)  # random 16-byte IV
    
    def _hash_key(self, key):
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(key.encode('utf-8'))
        return digest.finalize()[:16]

    def _pad(self, data):
        block_size = 16
        pad_len = block_size - len(data) % block_size
        padding = bytes([pad_len]) * pad_len
        return data + padding

    def _unpad(self, data):
        pad_len = data[-1]
        return data[:-pad_len]

    def encrypt(self, plaintext):
        padded_plaintext = self._pad(plaintext.encode('utf-8'))
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
        return base64.b64encode(self.iv + ciphertext) #prepend the IV to the ciphertext and encode to base64

    def decrypt(self, ciphertext):
        # Decode the base64 and separate the IV from the ciphertext
        ciphertext = base64.b64decode(ciphertext)
        iv = ciphertext[:16]  # Extract the IV (first 16 bytes)
        actual_ciphertext = ciphertext[16:]

        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_padded = decryptor.update(actual_ciphertext) + decryptor.finalize()
        plaintext = self._unpad(decrypted_padded)
        return plaintext.decode('utf-8')
