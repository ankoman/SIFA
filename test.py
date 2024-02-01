from aes import AES

def main():
    master_key = 0x000102030405060708090a0b0c0d0e0f
    aes = AES(master_key)

    plaintext = 0x00112233445566778899aabbccddeeff
    encrypted = aes.encrypt(plaintext)
    print(f"{encrypted:032x}")

    decrypted = aes.decrypt(encrypted)
    print(f"{decrypted:032x}")

if __name__ == '__main__':
    main()