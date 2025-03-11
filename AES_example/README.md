# AES Simplified Implementation
##### This folder contains a simplified implementation of AES128 using the Cipher Block Chaining (CBC) mode of operation

## For info on AES, please read "**about_AES.md**" (Brief research report)

## Files:
### **AES_test_v1.py**
> AES128 implementation utilizing (and heavily relies upon) the "cryptography" python library
### **AES_test_v2.py**
> AES128 implementation that does NOT rely on the "cryptography" python library
### **AES_runner.py**
> Runs both AES_test version files and prints the their respective ciphertext outputs, as well as their decrypted outputs 
### **AES_keygen.py**
> Generates a symmetric key for AES128
### **s_box.py**
> S-box and Inverse S-box Generation
### **cleanup.py**
> Removes certain .txt files
### **about_AES.md**
> Contains additional info (very short research report) on AES
### **requirements.txt**

## How to run:
Create a py environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

pip install 
Install dependencies - cryptography: 
```bash
pip install -r requirements.txt
```

Create 'plaintext.txt' and write a message you would like to encrypt

Generate a key:
```bash
python ./AES_keygen.py
```

Run the Encryption/Decryption Runner:
```bash
python ./AES_runner.py
```

> This will print out the encrypted message, as well as its decrypted counterpart
'ciphertext.txt' will only contain ciphertext (From v1 and v2)
There will be two decrypted outputs; 'decrypted_v1.txt' and 'decrypted_v2.txt' from AES_test_v1.py and AES_test_v2.py respectively

To compare if decryption process was successful:
```bash
diff decrypted_v1.txt plaintext.txt
diff decrypted_v2.txt plaintext.txt
```

To cleanup after:
```bash
python ./cleanup.py
```

> This script removes the following files: "key.txt", "decrypted_v1.txt", "decrypted_v2.txt", "ciphertext.txt"

To stop the python environment (venv):
```bash
deactivate
```