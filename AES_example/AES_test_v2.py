import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

class AESCipher(object):

    def __init__(self, key):
        # AES block size (128 bits or 16 bytes)
        self.bs = AES.block_size
        # The provided key is hashed using SHA-256 to make sure it is 32 bytes (256 bits)
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        # Pad the input data so that its length is a multiple of AES block size
        raw = self._pad(raw)
        # Generate a random initialization vector (IV) for encryption (AES block size)
        iv = Random.new().read(AES.block_size)
        # Create the AES cipher object in CBC mode with the key and IV
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        # Encrypt the data and prepend the IV to the ciphertext
        # Return the result as a base64-encoded string for easy handling
        return base64.b64encode(iv + cipher.encrypt(raw.encode()))

    def decrypt(self, enc):
        # Decode the base64-encoded ciphertext
        enc = base64.b64decode(enc)
        # Extract the IV from the first block (AES block size)
        iv = enc[:AES.block_size]
        # Create the AES cipher object in CBC mode with the key and IV
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        # Decrypt the ciphertext (after the IV) and remove padding
        return AESCipher._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        # Apply PKCS7 padding: Add enough padding bytes to make the length a multiple of the block size
        # The number of padding bytes equals the difference between block size and the remainder
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        # Remove the padding added during encryption by inspecting the last byte (the padding length)
        return s[:-ord(s[len(s)-1:])]