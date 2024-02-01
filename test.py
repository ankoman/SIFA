from aes import AES, text2matrix, matrix2text

def main():
    master_key = 0x000102030405060708090a0b0c0d0e0f
    aes = AES(master_key)

    ival_before_9thMC = 0x00112233445566778899aabbccddeeff
    aes.state_matrix = text2matrix(ival_before_9thMC)
    print(aes.state_matrix)

    aes._AES__add_round_key(aes.state_matrix, aes.round_keys[:4])

    aes._AES__sub_bytes(aes.state_matrix)
    aes._AES__shift_rows(aes.state_matrix)
    aes._AES__mix_columns(aes.state_matrix)
    aes._AES__add_round_key(aes.state_matrix, aes.round_keys[4 * 1 : 4 * (1 + 1)])

    print(f"{matrix2text(aes.state_matrix):x}")

    # Correct ctxt = round[ 2].start 89d810e8855ace682d1843d8cb128fe4

if __name__ == '__main__':
    main()