from aes import AES, text2matrix, matrix2text
import random

master_key = 0x000102030405060708090a0b0c0d0e0f
aes = AES(master_key)
round_key = [aes.round_keys[4 * 1 : 4 * (1 + 1)] for i in range(3)]
print(f"Traget key: {matrix2text(round_key[2]):x}")

def simplified_aes(ptxt, fault_injected = 0):

    ival_before_9thMC = ptxt
    aes.state_matrix = text2matrix(ival_before_9thMC)

    aes._AES__add_round_key(aes.state_matrix, round_key[0])

    aes._AES__sub_bytes(aes.state_matrix)
    aes._AES__shift_rows(aes.state_matrix)
    #print(f"{matrix2text(aes.state_matrix):032x}")
    if fault_injected:
        aes.state_matrix[0][1] = 0
    #print(f"{matrix2text(aes.state_matrix):032x}")

    aes._AES__mix_columns(aes.state_matrix)
    aes._AES__add_round_key(aes.state_matrix, round_key[1])

    # Omit SB & SR to ease the experiments
    aes._AES__add_round_key(aes.state_matrix, round_key[2])

    return aes.state_matrix 

def main():
    list_ineffective = []

    for i in range(256 * 200):
        ptxt = random.randint(0, 2**128 - 1)
        #print(f"{ptxt:x}")
        C = simplified_aes(ptxt, fault_injected = 0)
        Cp = simplified_aes(ptxt, fault_injected = 1)
        if C == Cp:
            # ineffective
            list_ineffective.append(Cp)


    for key in range(10000):
        for ctxt in list_ineffective:





if __name__ == '__main__':
    main()