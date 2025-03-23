from Crypto.PublicKey import RSA

def generate_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    # Save keys to files
    with open('private.pem', 'wb') as f:
        f.write(private_key)

    with open('public.pem', 'wb') as f:
        f.write(public_key)

    print("Keys generated and saved to 'private.pem' and 'public.pem'.")
