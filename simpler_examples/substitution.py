import random
import string

# Creates a random permutation when ran, stores as a dictionary 
# with keys the alphabet and values the permuted alphabet
def random_permutation():
    a_to_n = list(string.ascii_lowercase)
    a_to_b = {}
    l = set()
    j = 0
    while len(l) < 26:
        permuted_letter = a_to_n[random.randrange(0, 26)]
        if permuted_letter not in l:
            l.add(permuted_letter)
            a_to_b[a_to_n[j]] = permuted_letter
            j += 1
    return a_to_b

# Input a dictionary d giving a permutation of the lower case alphabet
# Outputs a substitution cipher applied to the string st
def substitution_cipher(d, st):
    st = st.lower()
    l = list(st)
    code_w = [d[n] if n in d else n for n in l]
    st = ''.join(code_w)
    return st

# Prints the frequency of characters appearing in cipher
def check_frequency(st):
    a_to_n = list(string.ascii_lowercase)
    l = list(st)
    d = {}
    j = 0
    for i in l:
        if i in a_to_n:
            d[i] = d.get(i, 0) + 1
            j += 1
    for i in d:
        d[i] = d[i] / j
    return d

if __name__ == "__main__":
    plaintext = input("Input a message to encrypt: ")
    perm_dict = random_permutation()
    encrypted_text = substitution_cipher(perm_dict, plaintext)
    print(f"Encrypted text: {encrypted_text}")
    frequency = check_frequency(encrypted_text)
    print(f"Character frequencies: {frequency}")
