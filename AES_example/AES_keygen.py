def generate_aes_key():
  """Generates a random 128-bit AES key (16 bytes)."""
  key = bytearray(16)
  for i in range(16):
    key[i] = _get_random_byte()
  return bytes(key)

def _get_random_byte():
  """Generates a pseudo-random byte using system time."""
  return (int(str(time.time() % 1)[-1]) + ord(str(time.time() % 1)[-2])) % 256

if __name__ == '__main__':
    import time
    aes_key = generate_aes_key()
    print(f"Generated AES-128 key: {aes_key.hex()}")

    key_file = 'key.txt'
    with open(key_file, 'w') as file:
        file.write(aes_key.hex())