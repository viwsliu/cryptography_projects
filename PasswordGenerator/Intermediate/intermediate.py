import random
import string

def generate_password(length, use_uppercase, use_numbers, use_special_chars):
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special_chars = string.punctuation

    char_pool = lowercase
    if use_uppercase:
        char_pool += uppercase
    if use_numbers:
        char_pool += digits
    if use_special_chars:
        char_pool += special_chars

    password = []
    if use_uppercase:
        password.append(random.choice(uppercase))
    if use_numbers:
        password.append(random.choice(digits))
    if use_special_chars:
        password.append(random.choice(special_chars))

    password += random.choices(char_pool, k=length - len(password))

    random.shuffle(password)

    return ''.join(password)

if __name__ == "__main__":
    # print("test")
    password = generate_password(length=16, use_uppercase=True, use_numbers=True, use_special_chars=False)
    print(f"Generated Password: {password}")
