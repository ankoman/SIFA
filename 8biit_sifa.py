from aes import Sbox, InvSbox
from tqdm import tqdm
import random

dist_bin = [1, 8, 28, 56, 70, 56, 28, 8, 1]

ANALYSIS_MODEL = "2bits_joint"


def attack_location(x, correct_key, fault_injected = 0):
    if fault_injected:
        x |= random.randint(0, 0x1)
    y = Sbox[x]
    y ^= correct_key
    return y

def uniform_dist(x):
    if ANALYSIS_MODEL == "HW":
        return dist_bin[x] / 256
    elif ANALYSIS_MODEL == "LSB":
        return 1/2
    elif ANALYSIS_MODEL == "7bits":
        return 1/128
    elif ANALYSIS_MODEL == "2bits":
        return 1/4
    elif ANALYSIS_MODEL == "2bits_joint":
        return 1/4

def leak_f(x):
    if ANALYSIS_MODEL == "HW":
        return bin(x).count("1")
    elif ANALYSIS_MODEL == "LSB":
        return x & 0x1
    elif ANALYSIS_MODEL == "7bits":
        return x & 0x7f
    elif ANALYSIS_MODEL == "2bits":
        return x & 0x3
    elif ANALYSIS_MODEL == "2bits_joint":
        return (x & 0x2) >> 1

def get_SEI(key_hyp, list_ineffective, n_ineffective):
    if ANALYSIS_MODEL == "HW":
        n_leak_val = 9
    elif ANALYSIS_MODEL == "LSB":
        n_leak_val = 2
    elif ANALYSIS_MODEL == "7bits":
        n_leak_val = 128
    elif ANALYSIS_MODEL == "2bits":
        n_leak_val = 4
    elif ANALYSIS_MODEL == "2bits_joint":
        n_leak_val = 4

    ### Init dictionary
    list_freq = [0]*n_leak_val
    list_freq2 = [0]*n_leak_val

    for ctxt in list_ineffective:
        t0 = ctxt ^ key_hyp
        t1 = InvSbox[t0]
        ANALYSIS_MODEL == "LSB"
        leak = leak_f(t1)
        list_freq[leak] += 1
        ANALYSIS_MODEL == "2bits_joint"
        leak = leak_f(t1)
        list_freq2[leak] += 1

    ### Calc SEI
    sei = 0
    # for j in range(n_leak_val):
    #     sei += (list_freq[j]/n_ineffective - uniform_dist(j))**2
    sei += ((list_freq[0] + list_freq2[0])/n_ineffective - uniform_dist(0))**2
    sei += ((list_freq[0] + list_freq2[1])/n_ineffective - uniform_dist(0))**2
    sei += ((list_freq[1] + list_freq2[0])/n_ineffective - uniform_dist(0))**2
    sei += ((list_freq[1] + list_freq2[1])/n_ineffective - uniform_dist(0))**2

    return sei

def main():

    for n_enc in range(100, 2001, 100):
        ave_rank = 0
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

            for key_hyp in range(256):
                dict_SEI[hex(key_hyp)] = get_SEI(key_hyp, list_ineffective, n_ineffective)
            SEI_sorted = sorted(dict_SEI.items(), key=lambda x:x[1])[::-1]
            # print(f'Top 10 SEIs: {SEI_sorted[:9]}')

            ### Correct key rank
            rank = SEI_sorted.index((hex(correct_key), dict_SEI[hex(correct_key)])) + 1
            ave_rank += rank
            # print(f'Correct key rank: {rank}')

        ave_rank /= 256
        print(f"\n #{n_enc} Average rank = {ave_rank}")

if __name__ == '__main__':
    main()