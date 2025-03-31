import sys
from cryptography.fernet import Fernet

def main():
    if len(sys.argv) != 3:
        print("Usage: python encrypt.py <key_file> <passwords_file>")
        sys.exit(1)
    
    key_file = sys.argv[1]
    passwords_file = sys.argv[2]
    
    with open(key_file, "rb") as kf:
        key = kf.read().strip()
    
    fernet = Fernet(key)
    
    with open(passwords_file, "r") as pf:
        lines = pf.readlines()
    
    encrypted_lines = []
    for line in lines:
        line = line.strip()
        if line:
            encrypted = fernet.encrypt(line.encode()).decode()
            encrypted_lines.append(encrypted)
        else:
            encrypted_lines.append("")
    
    with open(passwords_file, "w") as pf:
        for enc_line in encrypted_lines:
            pf.write(enc_line + "\n")

if __name__ == "__main__":
    main()