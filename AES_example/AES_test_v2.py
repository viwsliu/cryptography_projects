from cryptography.hazmat.primitives import hashes 
# https://cryptography.io/en/latest/hazmat/primitives/cryptographic-hashes/#cryptography.hazmat.primitives.hashes.Hash
from cryptography.hazmat.backends import default_backend

from copy import copy
import base64 # used to encode/decode binary data to/from ASCII text
import s_box #python helper functions to generate S-boxes and Inverse S-boxes
import os

import key_expansion as key_expan #python helper functions for key_expansion step

class AESEncryption(object):
    def __init__(self, key):
        self.key = self._hash_key(key)
        self.iv = os.urandom(16)  # randomly generated 16-byte IV
        self.turns = 10  # 128-bit key means 10 rounds of encryption
        self.s_box, self.inv_s_box = s_box.generate_sbox()
        self.write_to_sbox_file()

        self.state = None

        temp_key = [key[i:i+2] for i in range(0, len(key), 2)]
        self.key_expansion = key_expan.keyExpansion(temp_key)
        # print(self.key_expansion)

    def write_to_sbox_file(self): #write the used S-Box and Inverse S-Box used
        s_box_file = 's_boxes_used.txt'
        with open(s_box_file, 'w') as file:
            file.write('Encrypted v2 s_box: \n')
            for i, item in enumerate(self.s_box, start=1):
                file.write(f'{hex(item)} ')
                if i % 16 == 0:
                    file.write('\n')
            file.write('\n')
            file.write('v2 inverse s_box: \n')
            for i, item in enumerate(self.inv_s_box, start=1):
                file.write(f'{hex(item)} ')
                if i % 16 == 0:
                    file.write('\n')
        return
    
    def _hash_key(self, key): #takes a 128 bit key and produces a hashed output using SHA-256
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(key.encode('utf-8')) #converts input key to bytes using UTF-8 endcoding, since hash functions work on byte data
        return digest.finalize()[:16]  #only return the first 16 bytes (128 bits of the hash)
    
    def _pad(self, data): # implements PKS-57 padding. used when plaintext is not a multiple of 16 bytes
        block_size = 16 # standard block size of AES
        pad_len = block_size - len(data) % block_size # calculate how many bytes are needed to reach the next multiple of 16
        padding = bytes([pad_len]) * pad_len
        return data + padding #returns plaintext + padding

    def unpad(self, data): #takes decrypted text with padding and removes padding found in last 16 bytes
        padding_length = data[-1]
        if padding_length < 1 or padding_length > 16:
            raise ValueError("Error in unpad")
        return data[:-padding_length]

    def subBytes(self, state): # apply s-box substitution to each byte in the state (data being processed during each step of the AES algorithm)
        for i in range(len(state)):
            state[i] = self.s_box[state[i]]

    def subBytesInv(self, state): # apply inverse s-box substitution to each byte in the state
        for i in range(len(state)):
            state[i] = self.inv_s_box[state[i]]

    def rotate(self, word, n): # rotates a 4-byte word by 'n' positions
        return word[n:] + word[:n]

    def shiftRows(self, state): #Shift rows
        for i in range(4):
            state[i * 4:(i + 1) * 4] = self.rotate(state[i * 4:(i + 1) * 4], i)

    def shiftRowsInv(self, state): #Inverse shift rows
        for i in range(4):
            state[i * 4:(i + 1) * 4] = self.rotate(state[i * 4:(i + 1) * 4], -i)

    def galoisMult(self, a, b): # galois field multiplication 
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

    def mixColumn(self, column): # Mixes the input column of the state matrix using GF multiplication
        # each element of the column is multiplied by a constant (2, 3, 1, 1) and combined using XOR
        temp = copy(column)
        column[0] = self.galoisMult(temp[0], 2) ^ self.galoisMult(temp[3], 1) ^ self.galoisMult(temp[2], 1) ^ self.galoisMult(temp[1], 3)
        column[1] = self.galoisMult(temp[1], 2) ^ self.galoisMult(temp[0], 1) ^ self.galoisMult(temp[3], 1) ^ self.galoisMult(temp[2], 3)
        column[2] = self.galoisMult(temp[2], 2) ^ self.galoisMult(temp[1], 1) ^ self.galoisMult(temp[0], 1) ^ self.galoisMult(temp[3], 3)
        column[3] = self.galoisMult(temp[3], 2) ^ self.galoisMult(temp[2], 1) ^ self.galoisMult(temp[1], 1) ^ self.galoisMult(temp[0], 3)

    def mixColumnInv(self, column): # Mixes the input column of the state matrix using inverse GF multiplication
        # inverse matrix is used to restore the original data by multiplying by constants (14, 11, 13, 9) and combining results using XOR.
        temp = copy(column)
        column[0] = self.galoisMult(temp[0], 14) ^ self.galoisMult(temp[3], 9) ^ self.galoisMult(temp[2], 13) ^ self.galoisMult(temp[1], 11)
        column[1] = self.galoisMult(temp[1], 14) ^ self.galoisMult(temp[0], 9) ^ self.galoisMult(temp[3], 13) ^ self.galoisMult(temp[2], 11)
        column[2] = self.galoisMult(temp[2], 14) ^ self.galoisMult(temp[1], 9) ^ self.galoisMult(temp[0], 13) ^ self.galoisMult(temp[3], 11)
        column[3] = self.galoisMult(temp[3], 14) ^ self.galoisMult(temp[2], 9) ^ self.galoisMult(temp[1], 13) ^ self.galoisMult(temp[0], 11)

    def addRoundKey(self, state_1d, round_key):
        state = [state_1d[i:i + 4] for i in range(0, len(state_1d), 4)]
        new_state = []
        # print("state", state)
        # print("round_key", round_key)
        for i in range(4):
            row = []
            for j in range(4):
                round_key_byte = int(round_key[i][j], 16)
                xor_result = state[i][j] ^ round_key_byte
                row.append(xor_result)
            new_state.append(row)
        return new_state

    #(still trying to figure out key expansion step)
    def encrypt(self, plaintext):
        plaintext = self._pad(plaintext.encode('utf-8'))  # pad plaintext to make it a multiple of 16 bytes
        encrypted_data = b""
        for i in range(0, len(plaintext), 16):
            block = plaintext[i:i + 16]  # extract 16-byte block
            state = list(block)  # convert each 16-byte block into list of bytes
            self.addRoundKey(state, self.key_expansion)
            for round in range(self.turns - 1):  # 9 rounds of AES encryption (since we already did initial round)
                self.subBytes(state)
                self.shiftRows(state)
                self.mixColumn(state)
                self.addRoundKey(state, self.key_expansion)
            #no mixColumn in final round
            self.subBytes(state)
            self.shiftRows(state)
            self.addRoundKey(state, self.key_expansion)
            encrypted_data += bytes(state)
        return base64.b64encode(self.iv + encrypted_data).decode('utf-8')  # Return encrypted data with IV

    def decrypt(self, encoded_ciphertext):
        decoded_data = base64.b64decode(encoded_ciphertext)  # Decode base64 encoded ciphertext and extract the IV and ciphertext
        iv = decoded_data[:16]  # First 16 bytes are the IV
        ciphertext = decoded_data[16:]  # The rest is the ciphertext
        decrypted_data = b""
        # Process in 16-byte blocks
        for i in range(0, len(ciphertext), 16):
            block = ciphertext[i:i + 16]  # extract 16-byte block
            state = list(block)  # convert each 16-byte block into list of bytes
            self.addRoundKey(state, self.key_expansion)
            for round in range(self.turns - 1):  # 9 rounds of AES decryption
                self.shiftRowsInv(state)
                self.subBytesInv(state)
                self.addRoundKey(state, self.key_expansion)
                self.mixColumnInv(state)
            #no mixColumn in final round
            self.shiftRowsInv(state)
            self.subBytesInv(state)
            self.addRoundKey(state, self.key_expansion)
            decrypted_data += bytes(state)  #append decrypted block to output
        return self.unpad(decrypted_data).decode('utf-8') #remove padding and return decrypted text

#testing
if __name__ == "__main__":
    
    input_key_file = 'key.txt' 
    with open(input_key_file, 'r') as file:
        key = file.read()

    test = AESEncryption(key)

    input_file = 'plaintext.txt'
    with open(input_file, 'r') as file:
        input_data = file.read()

    encrypted = test.encrypt(input_data)
    print(f'\n Encrypted v2: {encrypted} \n')

    decrypted = test.decrypt(encrypted)
    print(f'Decrypted v2: {decrypted} \n')