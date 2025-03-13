import s_box as s_box_gen  # Using my own S_Box generator

sbox, inv_s_box = s_box_gen.generate_sbox()

Rcon = [
    0x00000000, 0x01000000, 0x02000000,
    0x04000000, 0x08000000, 0x10000000,
    0x20000000, 0x40000000, 0x80000000,
    0x1b000000, 0x36000000
]

#This file performs the key expansion set of AES. Contains additional helper functions required for the step as well
def keyExpansion(key):
    w = [[] for _ in range(44)]
    for i in range(4):
        w[i] = [key[4*i], key[4*i+1], key[4*i+2], key[4*i+3]]
    for i in range(4, 44):
        temp = w[i-1]
        word = w[i-4]
        if i % 4 == 0:
            x = RotWord(temp)
            y = SubWord(x)
            rcon = Rcon[int(i/4)]
            temp = hexor(y, hex(rcon)[2:])
        word = ''.join(word)
        temp = ''.join(temp)
        xord = hexor(word, temp)
        w[i] = [xord[:2], xord[2:4], xord[4:6], xord[6:8]]
    return w

def hexor(hex1, hex2):
    bin1 = hex2binary(hex1)
    bin2 = hex2binary(hex2)
    xord = int(bin1, 2) ^ int(bin2, 2)
    hexed = hex(xord)[2:]
    if len(hexed) != 8:
        hexed = '0' + hexed
    return hexed

def hex2binary(hex):
    return bin(int(str(hex), 16))

def RotWord(word):
    return word[1:] + word[:1]

def SubWord(word):
    sWord = ()
    for i in range(4):
        if word[i][0].isdigit() == False:
            row = ord(word[i][0]) - 86
        else:
            row = int(word[i][0]) + 1
        if word[i][1].isdigit() == False:
            col = ord(word[i][1]) - 86
        else:
            col = int(word[i][1]) + 1
        sBoxIndex = (row*16) - (17-col)
        piece = hex(sbox[sBoxIndex])[2:]
        if len(piece) != 2:
            piece = '0' + piece
        sWord = (*sWord, piece)
    return ''.join(sWord)

def prettyPrint(w):
    print("\n\nKeywords: \n")
    for i in range(len(w)):
        print("w" + str(i), "=", w[i][0], w[i][1], w[i][2], w[i][3])

def split_string(s):
    return [s[i:i+2] for i in range(0, len(s), 2)]

def pair_string(input_string):
    if len(input_string) != 32:
        raise ValueError("Input string must be 32 characters long")
    paired_list = [input_string[i:i+2] for i in range(0, len(input_string), 2)]
    return paired_list

if __name__ == "__main__":
    input_key_file = 'key.txt'
    with open(input_key_file, 'r') as file:
        key = file.read()
    key = [key[i:i+2] for i in range(0, len(key), 2)]
    w = keyExpansion(key)
    print(w)
    prettyPrint(w)
