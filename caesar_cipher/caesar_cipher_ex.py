from secretpy import Caesar

class CaesarCipher:
    def __init__(self, key, alphabet):
        self.key = key
        self.alphabet = alphabet
        self.caesar = Caesar()

    def encrypt(self, plaintext):
        return self.caesar.encrypt(plaintext, self.key, self.alphabet)

    def decrypt(self, ciphertext):
        return self.caesar.decrypt(ciphertext, self.key, self.alphabet)

if __name__ == "__main__":
    plaintext = input("Enter plaintext: ")
    key = 5
    alphabet = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ' ')

    cipher = CaesarCipher(key, alphabet)
    ciphertext = cipher.encrypt(plaintext)
    print(f"Encrypted Caesar ciphertext: {ciphertext}")

    decrypted_text = cipher.decrypt(ciphertext)
    print(f"Decrypted Caesar plaintext: {decrypted_text}")