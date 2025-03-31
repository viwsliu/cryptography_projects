# Password encryptor
Scripts provide a basic but secure method to protect your stored passwords. Users can store their passwords in a .xlsx file and encrypt/decrypt specific columns. It will be the user's responsibility to safeguard their key, as it is essential for both encryption/decryption.

## Usage Instructions

### Generate a key (if needed):
1. Generate/Insert Key
If you do not have a key, run the generate_key.py script to create a key file (e.g., mykey.key)
If you do have a key, write it into mykey.key

2. Encrypt the passwords file:
```bash
python encrypt.py keyfile_name.key plaintext_passwords.xlsx Column_Name
```
This replaces the contents of plaintext_passwords.xlsx with the encrypted data

3. Decrypt the passwords file:
```bash
python decrypt.py keyfile_name.key encrypted_passwords.xlsx Column_Name
```
This restores the original plaintext passwords in passwords.xlsx 