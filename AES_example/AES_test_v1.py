from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import os

class AESEncryption(object):
    def __init__(self, key):
        # Initialize the class with the provided key
        self.key = self._hash_key(key)
        self.iv = os.urandom(16)  # Generate a random 16-byte IV
    
    def _hash_key(self, key):
        # Hash the key to ensure it's 16 bytes long (128 bits)
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(key.encode('utf-8'))
        return digest.finalize()[:16]  # Use the first 16 bytes of the SHA256 hash

    def encrypt(self, plaintext):
        # Create a Cipher object for AES encryption in CBC mode with the key and IV
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv), backend=default_backend())
        encryptor = cipher.encryptor()
        
        # Pad the plaintext to be a multiple of the AES block size (16 bytes)
        padder = padding.PKCS7(128).padder()
        padded_plaintext = padder.update(plaintext.encode('utf-8')) + padder.finalize()

        # Encrypt the padded plaintext
        ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
        return ciphertext

    def decrypt(self, ciphertext):
        # Create a Cipher object for AES decryption in CBC mode with the same key and IV
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv), backend=default_backend())
        decryptor = cipher.decryptor()

        # Decrypt the ciphertext
        decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()

        # Unpad the decrypted plaintext
        unpadder = padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(decrypted_padded) + unpadder.finalize()

        # Return the decrypted plaintext as a UTF-8 string
        return plaintext.decode('utf-8')
