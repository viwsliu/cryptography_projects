import os

def generate_aes_key(): #Generates a random 128-bit AES key (16 bytes)
    return os.urandom(16)

if __name__ == '__main__':
    key_file = 'key.txt'
    aes_key = generate_aes_key()
    print(f"Generated AES-128 key: {aes_key.hex()}")
    with open(key_file, 'w') as file:
        file.write(aes_key.hex())