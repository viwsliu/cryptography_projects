import sys
import pandas as pd
from cryptography.fernet import Fernet

def main():
    if len(sys.argv) != 4:
        print("Usage: python encrypt_excel.py <key_file> <excel_file> <column_name>")
        sys.exit(1)
    
    key_file = sys.argv[1]
    excel_file = sys.argv[2]
    column_name = sys.argv[3]

    with open(key_file, "rb") as f:
        key = f.read().strip()
    
    fernet = Fernet(key)
    
    try:
        df = pd.read_excel(excel_file)
    except Exception as e:
        print("Error reading Excel file:", e)
        sys.exit(1)
    
    if column_name not in df.columns:
        print(f"Column '{column_name}' not found in Excel file.")
        sys.exit(1)
    
    def encrypt_value(val):
        if pd.isna(val):
            return val
        return fernet.encrypt(str(val).encode()).decode()
    
    df[column_name] = df[column_name].apply(encrypt_value)
    
    try:
        df.to_excel(excel_file, index=False)
        print("Encryption complete.")
    except Exception as e:
        print("Error writing to Excel file:", e)

if __name__ == "__main__":
    main()
