#file containing helper functions for S-box and Inverse S-box generation

def generate_sbox():
    """ Generate an S-box (substitution box) and its inverse S-box. 
    Steps:
        >Find multiplicative inverse in the Galois Field GF(2^8)
        >Affine transformation
    """
    sbox = [0] * 256 #init S-box with 256 entries
    inv_sbox = [0] * 256 #init inverse S-box with 256 entries

    for i in range(256):
        inv = gf_multiply(i, 0x0E)  #calculate multiplicative inverse using GF(2^8)
        if inv != 0: #if the inverse exists, apply affine transformation, map inverse S-box
            sbox[i] = affine_transform(inv)
            inv_sbox[sbox[i]] = i
        else: #if no inverse exists use AES-defined constant for 0
            sbox[i] = 0x63

    return sbox, inv_sbox

def gf_multiply(x, y):
    """
    Multiply two numbers in Galois Field (2^8)
    x, y (ints): byte value between 0 and 255
    """
    result = 0
    for i in range(8):
        if (y & 1):
            result ^= x # XOR if LSB of y is 1
        x = xtime(x) # multiply x by 2
        y >>= 1 # shift y right by 1 to process the next bit
    return result

def xtime(x):
    """
    Multiply by 2 in GF(2^8)
    x (int): input byte between 0 and 255
    """
    return ((x << 1) & 0xFF) ^ (0x1B if (x & 0x80) else 0)

def affine_transform(x):
    """
    Apply affine transformation for S-box. Transformation is a bitwise operation that scrambles the input
    x (int): input byte between 0 and 255
    """
    # bitwise XOR with right-shifted versions of x
    x ^= (x >> 4)
    x ^= (x >> 5)
    x ^= (x >> 6)
    x ^= (x >> 7)

    # final XOR with the constant 0x63 (as defined by AES standard)
    x = (x & 0xFF) ^ 0x63
    return x