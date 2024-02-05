from aes import AES, text2matrix, matrix2text
from tqdm import tqdm
import random


master_key = 0x000102030405060708090a0b0c0d0e0f
aes = AES(master_key)
round_key = [aes.round_keys[4 * 1 : 4 * (1 + 1)] for i in range(3)]
target_key = matrix2text(round_key[2])
print(f"Traget key: {target_key:x}")

def simplified_aes(ptxt, fault_injected = 0):

    ival_before_9thMC = ptxt
    aes.state_matrix = text2matrix(ival_before_9thMC)

    aes._AES__add_round_key(aes.state_matrix, round_key[0])

    aes._AES__sub_bytes(aes.state_matrix)
    aes._AES__shift_rows(aes.state_matrix)
    #print(f"{matrix2text(aes.state_matrix):032x}")
    if fault_injected:
        aes.state_matrix[0][1] &= 0xf7
    #print(f"{matrix2text(aes.state_matrix):032x}")

    aes._AES__mix_columns(aes.state_matrix)
    aes._AES__add_round_key(aes.state_matrix, round_key[1])

    # Omit SB & SR to ease the experiments
    aes._AES__add_round_key(aes.state_matrix, round_key[2])

    return aes.state_matrix 

def get_SEI(key, list_ineffective, n_ineffective):
    key = text2matrix(key)

    ### Init dictionary
    dict_freq = {}
    for j in range(256):
        dict_freq[j] = 0

    for ctxt in list_ineffective:
        aes._AES__add_round_key(ctxt, key)
        aes._AES__inv_mix_columns(ctxt)
        dict_freq[ctxt[0][1]] += 2

    ### Calc SEI
    sei = 0
    for j in range(256):
        sei += (dict_freq[j]/n_ineffective - 1/256)**2
    return sei

def main():
    list_ineffective = []
    dict_SEI = {}

    n_trial = 256 * 1
    for i in range(n_trial):
        ptxt = random.randint(0, 2**128 - 1)
        #print(f"{ptxt:x}")
        C = simplified_aes(ptxt, fault_injected = 0)
        Cp = simplified_aes(ptxt, fault_injected = 1)
        if C == Cp:
            # ineffective
            list_ineffective.append(Cp)
    n_ineffective = len(list_ineffective)
    print(f'{n_ineffective} ineffective faults out of {n_trial} fault injection ({n_ineffective/n_trial*100} %)')

    n = 100000
    for i in tqdm(range(n)):
        key = random.randint(0, 2**128 - 1)
        dict_SEI[hex(key)] = get_SEI(key, list_ineffective, n_ineffective)
    SEI_sorted = sorted(dict_SEI.items(), key=lambda x:x[1])
    print(f'Top 10 wrong key SEIs: {SEI_sorted[:9]}')

    ### Correct key SEI
    sei = get_SEI(target_key, list_ineffective, n_ineffective)
    print(f'Correct key SEI = {sei}')


if __name__ == '__main__':
    main()