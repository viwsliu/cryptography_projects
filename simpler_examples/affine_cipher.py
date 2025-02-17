import string

# Applies affine cipher with scaling factor m, shifting factor k to string st
def affine_cipher(m, k, st):
    a_to_n = dict(zip(string.ascii_lowercase, range(26)))
    n_to_a = {v: k for k, v in a_to_n.items()}
    st = st.lower()
    num_l = [a_to_n.get(n, n) for n in st]
    num_aff = [(m * i + k) % 26 if isinstance(i, int) else i for i in num_l]
    encrypted = ''.join([n_to_a.get(n, n) if isinstance(n, int) else n for n in num_aff])
    return encrypted

if __name__ == "__main__":
    plaintext = input("Input a message to encrypt: ")
    m = int(input("Enter the scaling factor (m): "))
    k = int(input("Enter the shifting factor (k): "))
    encrypted_message = affine_cipher(m, k, plaintext)
    print(f"Encrypted message: {encrypted_message}")
