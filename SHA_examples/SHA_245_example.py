from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

message_1 = input("Input first message: ").encode('utf-8')
message_2 = input("Input second message: ").encode('utf-8')

#Helper function that returns the number of characters different in two strings
def char_diff(str1, str2):
    return sum ( str1[i] != str2[i] for i in range(len(str1)) )

# Create new SHA-256 hash objects, one for each message
chf_1 = hashes.Hash(hashes.SHA256(), backend=default_backend())
chf_2 = hashes.Hash(hashes.SHA256(), backend=default_backend())

# Update each hash object with the bytes of the corresponding message
chf_1.update(message_1)
chf_2.update(message_2)

# Finalize the hash process and obtain the digests
digest_1 = chf_1.finalize()
digest_2 = chf_2.finalize()

#Convert the resulting hash to hexadecimal strings for convenient printing
digest_1_str = digest_1.hex()
digest_2_str = digest_2.hex()

#Print out the digests as strings 
print(f"digest-1: {digest_1_str}")
print(f"digest-2: {digest_2_str}")

print(f"The two digests differ by { char_diff(digest_1_str, digest_2_str)} characters")