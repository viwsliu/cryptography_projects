from cryptography.fernet import Fernet

key = Fernet.generate_key()
with open("mykey.key", "wb") as key_file:
    key_file.write(key)
print("Key generated and saved to mykey.key")