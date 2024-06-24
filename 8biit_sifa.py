from aes import Sbox, InvSbox
from tqdm import tqdm
import random

dist_bin = [1, 8, 28, 56, 70, 56, 28, 8, 1]

ANALYSIS_MODEL = "2bits"


def attack_location(x, correct_key, fault_injected = 0):
    if fault_injected:
        x &= 0xfe#random.randint(0,0x3)
    y = Sbox[x]
    y ^= correct_key
    return y

def uniform_dist(x):
    if ANALYSIS_MODEL == "HW":
        return dist_bin[x] / 256
    elif ANALYSIS_MODEL == "LSB":
        return 1/2
    elif "bits" in ANALYSIS_MODEL:
        n_bits = int(ANALYSIS_MODEL[0])
        return 1/(2**n_bits)

def leak_f(x):
    if ANALYSIS_MODEL == "HW":
        return bin(x).count("1")
    elif ANALYSIS_MODEL == "LSB":
        return x & 0x1
    elif "bits" in ANALYSIS_MODEL:
        n_bits = int(ANALYSIS_MODEL[0])
        return x & (2**n_bits - 1)

def get_SEI(key_hyp, list_ineffective, n_ineffective):
    if ANALYSIS_MODEL == "HW":
        n_leak_val = 9
    elif ANALYSIS_MODEL == "LSB":
        n_leak_val = 2
    elif "bits" in ANALYSIS_MODEL:
        n_bits = int(ANALYSIS_MODEL[0])
        n_leak_val = 2**n_bits

    ### Init dictionary
    list_freq = [0]*n_leak_val

    for ctxt in list_ineffective:
        t0 = ctxt ^ key_hyp
        t1 = InvSbox[t0]
        leak = leak_f(t1)
        list_freq[leak] += 1

    # ### Calc SEI
    # sei = 0
    # for j in range(n_leak_val):
    #     sei += (list_freq[j]/n_ineffective - uniform_dist(j))**2
    # return sei

    ### Calc CHI
    chi = 0
    for j in range(n_leak_val):
        chi += ((list_freq[j]/n_ineffective - uniform_dist(j))**2) / uniform_dist(j)
    return chi*n_ineffective


def main():

    for n_enc in range(100, 2001, 100):
        ave_rank = 0
        ave_sei_1st = 0
        ave_sei_2nd = 0
        for correct_key in range(256):
            #print(f"\nCorrect key: {correct_key:x}")
            list_ineffective = []
            dict_SEI = {}

            for i in range(n_enc):
                int_state = random.randint(0, 256 - 1)
                #print(f"{ptxt:x}")
                C = attack_location(int_state, correct_key, fault_injected = 0)
                Cp = attack_location(int_state, correct_key, fault_injected = 1)
                if C == Cp:
                    # ineffective
                    list_ineffective.append(Cp)
            n_ineffective = len(list_ineffective)
            # print(f'{n_ineffective} ineffective faults out of {n_enc} fault injection ({n_ineffective/n_enc*100} %)')

            if n_ineffective > 0:
                for key_hyp in range(256):
                    dict_SEI[hex(key_hyp)] = get_SEI(key_hyp, list_ineffective, n_ineffective)
                SEI_sorted = sorted(dict_SEI.items(), key=lambda x:x[1])[::-1]
                # print(f'Top 10 SEIs: {SEI_sorted[:9]}')

                ### Correct key rank
                rank = SEI_sorted.index((hex(correct_key), dict_SEI[hex(correct_key)])) + 1
                sei_1st = SEI_sorted[0][1]
                sei_2nd = SEI_sorted[1][1]
            else:
                rank = 128
                sei_1st = 0
                sei_2nd = 0
            ave_rank += rank
            ave_sei_1st += sei_1st
            ave_sei_2nd += sei_2nd
            # print(f'Correct key rank: {rank}')

        ave_rank /= 256
        ave_sei_1st /= 256
        ave_sei_2nd /= 256
        print(f"\n #{n_enc} Average rank = {ave_rank}, Average sei_1st = {ave_sei_1st}, Average sei_2nd = {ave_sei_2nd}")

if __name__ == '__main__':
    main()