# Analysis & Implementation of the Advanced Encryption Standard: Rijndael
The Advanced Encryption Standard (AES), also known as Rijndael, is a symmetric key block cipher that was developed to replace the outdated and cryptographically insecure DES  (Data Encryption Standard), which was published in 1977. The cryptosystem was developed by two Belgian cryptographers; Joan Daemen and Vincent Rijmen. Published in 1998, AES was adopted by NIST (National Institute of Science and Technology) in 2001 (standardized in 2002) for its efficiency in both software and hardware, simplicity, and resistance to known cryptanalytic attacks. As of 2003, the NSA (National Security Agency) reviewed and announced the use of AES to protect classified information as well as top secret information. As of yet, AES is the first and only publicly accessible cipher.

## How It Works
AES is a symmetric-key algorithm that operates using a substitution-permutation network (SPN). AES does not utilize the Feistel network, which was the basis of older ciphers such as DES. An SPN repeatedly applies layers of substitution (obscure relationships between plaintext and ciphertext, aka “confusion”) and permutation (to diffuse data). AES encrypts data in fixed blocks of 128 bits and uses key sizes of 128, 192, or 256 bits. AES encrypts data in a 4x4 column-major array of 16 bytes (known as the “state”). The total number of transformation rounds depends on the key size; 10 rounds for a 128-bit key, 12 rounds for a 192-bit key, and 14 rounds for a 256-bit key. The encryption process is as follows:
1. Key Expansion - The original encryption key is expanded into a series of round keys using a recursive process. Each round key is used in its respective round of permutation.
2. AddRoundKey - The current state is XORed with a round key. This step integrates the encryption key into the transformation.
3. (Loop) From second to 9th, 11th or 13th rounds (128 bit, 192 bit, and 256 bit keys respectively):
    3a. SubBytes (Byte substitution) - Applies a non-linear substitution to each byte in the 4x4 state array using a predefined S-box (substitution box). This substitution helps obscure the relationship between the plaintext and ciphertext.
    3b. ShiftRows (Row shifting) - The last three rows of the state are shifted cyclically a certain number of steps. This step spreads the plaintext across the block, enhancing diffusion.
    3c. MixColumns (Column Mixing) - Each column of the state is treated as a polynomial and multiplied by a fixed polynomial in GF(2⁸) (Galois Field). This step combines the bytes within each column, making each output byte dependent on all input bytes in the column.
    3d. AddRoundKey (with corresponding round key)
4. SubBytes
5. ShiftRows
6. AddRoundKey

Decryption reverses these operations through a corresponding set of inverse rounds using the same key generated during the Key Expansion step. Each decryption round undoes the encryption steps in reverse order. Decryption process is as follows:

1. Inverse Key Expansion - The same key sequence from encryption is used, but the round keys are applied in reverse order, starting with the last round key
2. AddRoundKey - The ciphertext is XORed with the last round key
3. From the second-to-last to the second round (depending on the key size):
    3a. Inverse ShiftRows - The rows of the state are cyclically shifted right (opposite of the left shift in encryption), reversing the transposition
    3b. Inverse SubBytes - Each byte is replaced using the inverse S-box, undoing the byte substitution and restoring the original values
    3c. Inverse MixColumns - Each column of the state is multiplied by the inverse polynomial in GF(2⁸) to reverse the diffusion effect of the MixColumns step
    3d. AddRoundKey (with corresponding round key)
4. Inverse ShiftRows
5. Inverse SubBytes
6. AddRoundKey

By applying these inverse operations in the correct sequence, AES decrypts the ciphertext and recovers the original plaintext. This symmetry between encryption and decryption, combined with the complexity of the transformations, makes AES both efficient and secure against various forms of cryptanalysis.

## Modes of Operation

While AES is a block cipher, its practical application requires various modes of operation to handle different data sizes and ensure confidentiality and integrity. Some of the most commonly used modes include:

- Electronic Codebook (ECB): Each block of plaintext is encrypted independently with the same key. While easy to implement, it is vulnerable to pattern leakage (frequency attacks)
- Cipher Block Chaining (CBC): Enhances security by XORing each plaintext block with the previous ciphertext block before encryption. An initialization vector (IV) is used for the first block to avoid identical ciphertexts for identical plaintexts
- Cipher Feedback (CFB): Transforms a block cipher into a self-synchronizing stream cipher, where each part of the ciphertext depends on previous ciphertext values for decryption. It feeds part of the previous ciphertext back into the encryption process, which is then XORed with the plaintext to generate the ciphertext
- Output Feedback (OFB): Similar to CFB, it creates a synchronous stream cipher by using the output of the encryption algorithm (instead of the ciphertext) as the feedback. (Avoids error propagation but requires a good IV)
- Counter (CTR): Turns a block cipher into a stream cipher by generating a unique counter value for each block. The counter (used as an IV) is encrypted with a key, and the result is XORed with the plaintext to create the ciphertext.

## Known Attack Methods on AES

It is known that AES is not invulnerable to attacks, but remains a significant challenge to any potential adversaries. Known / Theoretical attacks include but are not limited to:

- Brute Force Attacks - When an attacker tries all possible keys until the correct one is identified. For AES-128, AES-192, and AES-256 it would take 2128, 2192, and 2256 operations respectively. These are computationally infeasible with current technology, but remain a theoretical concern.
- Side-Channel Attacks - Exploit physical information leaked during the encryption process, such as timing data, power consumption, or electromagnetic emissions. This type of attack was the only successful published attack against AES until May 2009.
- Related-Key Attacks - Exploits the simplicity of AES's key schedule and has a complexity of 2119 (Later improved to 299.5). In 2006, research presented the first known attacks on 7- and 8- round AES:Rijndael, as well as attacks on 8-round Rijndael for 192 and 256 bit keys.
- Biclique Attack (Meet in the Middle attack) - A type of meet-in-the-middle (MITM) attack that can be used to break reduced-round versions of AES. It has been demonstrated to work against versions of AES with fewer rounds but does not pose a significant risk to the full-round AES. Provides a slight advantage over brute force attacks.
- Preprint Attack [Theoretical] - Involves obtaining or exploiting partial information about the encryption key through some form of pre-encryption analysis or leakage. No practical success has been demonstrated against AES, and the concept remains as a theoretical vulnerability.
- Quantum Computing - Grover's Algorithm [Theoretical] - An attack algorithm could theoretically reduce the effective security of AES-256 to the level of AES-128, cutting the key search space in half. However, it is still considered a significant challenge, assuming sufficient key length, proper implementation, as well as the computational power required for the attacker.

Currently, there is no known practical attack that would allow someone without knowledge of the key to efficiently decrypt AES.


## Basis of Security

AES achieves its security through a combination of mathematical complexity and practical design considerations. The key elements that contribute to AES's strength are:

1. Substitution-Permutation Network (SPN)
    - AES utilizes a SPN structure, which alternates between substitution (using S-boxes) and permutation to create complex and non-linear transformations of the plaintext input.
2. Avalanche Effect
    - A cryptographic property where minor changes in the input result in substantial changes in the output (known as the diffusion property). AES is designed so that each bit of the ciphertext is influenced by every bit of the plaintext and the key. This design makes it extremely difficult for attackers to detect any patterns between the plaintext and ciphertext – protecting against known plaintext and frequency analysis attacks.
3. Key Space
    - AES uses key sizes of 128, 192, and 256 bits. The vast key space provided by these sizes makes AES resistant to brute force attacks. For example, for AES-128, the key space is computationally infeasible to break with current technology
4. Structural Complexity
    - AES's design includes at least nine rounds of substitution, permutation, and mixing operations to confuse and diffuse the relationship between plaintext and ciphertext. These operations resist cryptanalytic techniques like linear and differential cryptanalysis, with strong diffusion and the use of S-boxes making AES resistant to such attacks.


## References:

- ABI Software Development: AES (Advanced Encryption Standard) Simplified - Adam Berent (https://www.ime.usp.br/~rt/cranalysis/AESSimplified.pdf)
- Advanced Encryption System (AES) - Wikipedia (https://en.wikipedia.org/wiki/Advanced_Encryption_Standard)
- Improved Cryptanalysis of Rijndael - Niels Ferguson, John Kelsey, Stefan Lucks, Bruce Schneier, Mike Stay, David Wagner, and Doug Whiting (https://www.schneier.com/wp-content/uploads/2016/02/paper-rijndael.pdf)
-The difference in five modes in the AES encryption algorithm (https://www.highgo.ca/2019/08/08/the-difference-in-five-modes-in-the-aes-encryption-algorithm/)

