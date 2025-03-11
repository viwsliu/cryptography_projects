import os

delete_list = ["key.txt", "decrypted_v1.txt", "decrypted_v2.txt", "ciphertext.txt"]

current_directory = os.getcwd()

for filename in delete_list:
    file_path = os.path.join(current_directory, filename)
    if os.path.isfile(file_path):
        os.remove(file_path)
        print(f"Deleted {filename}")
    else:
        print(f"{filename} not found in the directory.")