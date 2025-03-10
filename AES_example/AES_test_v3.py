from cryptography.hazmat.primitives.ciphers import Cipher, modes, algorithms
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from copy import copy
import base64
import os
import s_box

class AESEncryption(object):

    def __init__(self, key):
        self.key = self._hash_key(key)
        self.iv = os.urandom(16)  # Random 16-byte IV
        self.turns = 10  # 128-bit key means 10 rounds of encryption
        self.s_box, self.inv_s_box = s_box.generate_sbox()
        self.state = None  # Initialize state properly

    def _hash_key(self, key):
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(key.encode('utf-8'))
        return digest.finalize()[:16]  # Use first 16 bytes (128 bits)

    def _pad(self, data):
        block_size = 16
        pad_len = block_size - len(data) % block_size
        padding = bytes([pad_len]) * pad_len
        return data + padding

    def _unpad(self, data):
        pad_len = data[-1]
        return data[:-pad_len]

    def subBytes(self, state):
        for i in range(len(state)):
            state[i] = self.s_box[state[i]]

    def subBytesInv(self, state):
        for i in range(len(state)):
            state[i] = self.inv_s_box[state[i]]

    def rotate(self, word, n):
        return word[n:] + word[:n]

    def shiftRows(self, state):
        for i in range(4):
            state[i * 4:(i + 1) * 4] = self.rotate(state[i * 4:(i + 1) * 4], i)

    def shiftRowsInv(self, state):
        for i in range(4):
            state[i * 4:(i + 1) * 4] = self.rotate(state[i * 4:(i + 1) * 4], -i)

    def galoisMult(self, a, b):
        p = 0
        for i in range(8):
            if b & 1:
                p ^= a
            hiBitSet = a & 0x80
            a <<= 1
            if hiBitSet:
                a ^= 0x1b
            b >>= 1
        return p % 256

    def mixColumn(self, column):
        temp = copy(column)
        column[0] = self.galoisMult(temp[0], 2) ^ self.galoisMult(temp[3], 1) ^ \
                    self.galoisMult(temp[2], 1) ^ self.galoisMult(temp[1], 3)
        column[1] = self.galoisMult(temp[1], 2) ^ self.galoisMult(temp[0], 1) ^ \
                    self.galoisMult(temp[3], 1) ^ self.galoisMult(temp[2], 3)
        column[2] = self.galoisMult(temp[2], 2) ^ self.galoisMult(temp[1], 1) ^ \
                    self.galoisMult(temp[0], 1) ^ self.galoisMult(temp[3], 3)
        column[3] = self.galoisMult(temp[3], 2) ^ self.galoisMult(temp[2], 1) ^ \
                    self.galoisMult(temp[1], 1) ^ self.galoisMult(temp[0], 3)

    def mixColumnInv(self, column):
        temp = copy(column)
        column[0] = self.galoisMult(temp[0], 14) ^ self.galoisMult(temp[3], 9) ^ \
                    self.galoisMult(temp[2], 13) ^ self.galoisMult(temp[1], 11)
        column[1] = self.galoisMult(temp[1], 14) ^ self.galoisMult(temp[0], 9) ^ \
                    self.galoisMult(temp[3], 13) ^ self.galoisMult(temp[2], 11)
        column[2] = self.galoisMult(temp[2], 14) ^ self.galoisMult(temp[1], 9) ^ \
                    self.galoisMult(temp[0], 13) ^ self.galoisMult(temp[3], 11)
        column[3] = self.galoisMult(temp[3], 14) ^ self.galoisMult(temp[2], 9) ^ \
                    self.galoisMult(temp[1], 13) ^ self.galoisMult(temp[0], 11)

    def addRoundKey(self, state, roundKey):
        for i in range(len(state)):
            state[i] ^= roundKey[i]

    def encrypt(self, plaintext):
        plaintext = self._pad(plaintext.encode('utf-8'))
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext) + encryptor.finalize()
        return base64.b64encode(self.iv + ciphertext).decode('utf-8')

    def decrypt(self, encoded_ciphertext):
        ciphertext = base64.b64decode(encoded_ciphertext)
        iv = ciphertext[:16]
        ciphertext = ciphertext[16:]
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        return self._unpad(plaintext).decode('utf-8')

