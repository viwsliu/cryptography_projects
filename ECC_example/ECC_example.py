# Elliptic Curve Cryptosystem (ECC) Implementation

import random

# Define the elliptic curve: y^2 = (x^3 + a*x + b) mod p
class EllipticCurve:
    def __init__(self, a, b, p):
        self.a = a  # Curve coefficient a
        self.b = b  # Curve coefficient b
        self.p = p  # Prime modulus (defines the finite field)

    # Check if a point (x, y) is on the curve
    def is_on_curve(self, x, y):
        return (y * y) % self.p == (x * x * x + self.a * x + self.b) % self.p

    # Add two points on the elliptic curve
    def add(self, P, Q):
        if P is None: return Q
        if Q is None: return P

        x1, y1 = P
        x2, y2 = Q

        if P == Q:  # Point doubling
            if y1 == 0: return None
            m = (3 * x1 * x1 + self.a) * pow(2 * y1, -1, self.p) % self.p
        else:  # Point addition
            if x1 == x2: return None
            m = (y2 - y1) * pow(x2 - x1, -1, self.p) % self.p

        x3 = (m * m - x1 - x2) % self.p
        y3 = (m * (x1 - x3) - y1) % self.p

        return (x3, y3)

    # Multiply a point by a scalar using the double-and-add algorithm
    def multiply(self, P, n):
        if P is None or n % self.p == 0:
            return None

        R = None  # Acts as the accumulator
        Q = P

        while n:
            if n & 1:  # If the current bit is set, add the point
                R = self.add(R, Q)
            Q = self.add(Q, Q)  # Double the point
            n >>= 1  # Shift right (divide by 2)

        return R

# ECC Key Generation
class ECC:
    def __init__(self, curve, G):
        self.curve = curve  # Elliptic curve
        self.G = G          # Base point (generator)

    def generate_keypair(self):
        private_key = random.randint(1, self.curve.p - 1)  # Private key (random scalar)
        public_key = self.curve.multiply(self.G, private_key)  # Public key (P = d * G)

        if public_key is None:
            raise ValueError("Failed to generate a valid public key")

        return private_key, public_key

    # ECC Encryption
    def encrypt(self, public_key, plaintext_point):
        k = random.randint(1, self.curve.p - 1)  # Random ephemeral key
        C1 = self.curve.multiply(self.G, k)  # C1 = k * G
        C2 = self.curve.add(plaintext_point, self.curve.multiply(public_key, k))  # C2 = M + k * P

        if C1 is None or C2 is None:
            raise ValueError("Encryption failed: Invalid point during encryption")

        return C1, C2

    # ECC Decryption
    def decrypt(self, private_key, C1, C2):
        S = self.curve.multiply(C1, private_key)  # Shared secret = d * C1

        if S is None:
            raise ValueError("Decryption failed: Invalid shared secret")

        S_neg = (S[0], -S[1] % self.curve.p)  # Negate the y-coordinate
        plaintext_point = self.curve.add(C2, S_neg)  # M = C2 - d * C1
        return plaintext_point

# Map characters to curve points (improved version to ensure valid points)
def char_to_point(char, curve):
    x = ord(char) % curve.p
    while True:
        for y in range(curve.p):
            if curve.is_on_curve(x, y):
                return (x, y)
        x = (x + 1) % curve.p  # Increment x to find a valid point

def point_to_char(point):
    if 32 <= point[0] <= 126:  # Ensure valid ASCII range
        return chr(point[0])
    else:
        raise ValueError("Decrypted point is out of valid ASCII range")

# File Encryption
def encrypt_file(input_file, output_file, ecc, public_key):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for char in infile.read():
            try:
                plaintext_point = char_to_point(char, ecc.curve)
                C1, C2 = ecc.encrypt(public_key, plaintext_point)
                if not (C1 and C2):
                    raise ValueError(f"Encryption failed for character: {char}")
                outfile.write(f"{C1[0]},{C1[1]},{C2[0]},{C2[1]}\n")
            except ValueError as e:
                print(f"Error: {e}")

# File Decryption
def decrypt_file(input_file, output_file, ecc, private_key):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            try:
                C1x, C1y, C2x, C2y = map(int, line.strip().split(','))
                decrypted_point = ecc.decrypt(private_key, (C1x, C1y), (C2x, C2y))
                outfile.write(point_to_char(decrypted_point))
            except ValueError as e:
                print(f"Decryption error: {e}")

# Example Usage
def main():
    # Define the elliptic curve y^2 = x^3 + 2x + 3 over F_97
    curve = EllipticCurve(a=2, b=3, p=97)

    # Base point G on the curve (for simplicity, we choose a known point)
    G = (3, 6)

    ecc = ECC(curve, G)

    # Generate key pairs
    try:
        private_key, public_key = ecc.generate_keypair()
        print(f"Private Key: {private_key}")
        print(f"Public Key: {public_key}")
    except ValueError as e:
        print(f"Key generation error: {e}")
        return

    # Encrypt and decrypt a file
    encrypt_file('input.txt', 'encrypted.txt', ecc, public_key)
    print("File encrypted successfully.")

    decrypt_file('encrypted.txt', 'decrypted.txt', ecc, private_key)
    print("File decrypted successfully.")

if __name__ == "__main__":
    main()
