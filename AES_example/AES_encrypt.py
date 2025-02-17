from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from functools import reduce
import numpy as np

class AESEncryption:
    def __init__(self, alphabet):
        self.alphabet = alphabet
        self.key = self._generate_key()
        self.iv = self._generate_key()

    def _generate_key(self):
        return reduce(lambda a, b: a + b, [np.random.choice(self.alphabet) for _ in range(16)])

    def encrypt(self, plaintext):
        cipher = Cipher(algorithms.AES(bytes(self.key, 'utf-8')), modes.CBC(bytes(self.iv, 'utf-8')))
        encryptor = cipher.encryptor()

        # Pad plaintext to 16 bytes (AES block size)
        padder = padding.PKCS7(128).padder()  # 128 bits = 16 bytes
        padded_plaintext = padder.update(plaintext.encode('utf-8')) + padder.finalize()

        ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
        return ciphertext

    def decrypt(self, ciphertext):
        cipher = Cipher(algorithms.AES(bytes(self.key, 'utf-8')), modes.CBC(bytes(self.iv, 'utf-8')))
        decryptor = cipher.decryptor()

        decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()

        # Unpad the plaintext
        unpadder = padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(decrypted_padded) + unpadder.finalize()

        return plaintext.decode('utf-8')
    
if __name__ == "__main__":
    plaintext = input("Enter plaintext: ")
    alphabet = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ' ')

    aes = AESEncryption(alphabet)
    ciphertext = aes.encrypt(plaintext)
    plaintext = aes.decrypt(ciphertext)
    print(f"AES Key: {aes.key}")
    print(f"AES IV: {aes.iv}")
    print(f"Encrypted AES ciphertext: {ciphertext}")
    print(f"Decrypted AES ciphertest: {plaintext}")