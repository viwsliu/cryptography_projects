import string

# Implements a shift cipher with shift k on string st
def shift_cipher(k, st):
    a_to_n = dict(zip(string.ascii_lowercase, range(26)))
    n_to_a = {v: k for k, v in a_to_n.items()}
    st = st.lower()
    num_l = [a_to_n.get(n, n) for n in st]
    num_shift = [(i + k) % 26 if isinstance(i, int) else i for i in num_l]
    encrypted = ''.join([n_to_a.get(n, n) if isinstance(n, int) else n for n in num_shift])
    return encrypted

# Decrypts a message by applying the inverse shift (k) to string st
def shift_decipher(k, st):
    a_to_n = dict(zip(string.ascii_lowercase, range(26)))
    n_to_a = {v: k for k, v in a_to_n.items()}
    num_l = [a_to_n.get(n, n) for n in st]
    num_shift = [(i - k) % 26 if isinstance(i, int) else i for i in num_l]
    decrypted = ''.join([n_to_a.get(n, n) if isinstance(n, int) else n for n in num_shift])
    return decrypted

if __name__ == "__main__":
    plaintext = str(input("Input a message to encrypt: "))
    k = int(input("how many digits to shift text? "))
    ciphertext = shift_cipher(k, plaintext)
    new_plaintext = shift_decipher(k, ciphertext)
    print(f"Encrypted text: {ciphertext}")
    print(f"Decrypted text: {new_plaintext}")
