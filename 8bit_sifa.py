from aes import Sbox, InvSbox
from tqdm import tqdm
import random
import math

dist_bin = [1, 8, 28, 56, 70, 56, 28, 8, 1]

ANALYSIS_MODEL = "3bits" ### ['n'bits_HW or 'n'bits]
print(ANALYSIS_MODEL)
n_bits = int(ANALYSIS_MODEL[0])
power_two = 2**n_bits

def HW(x):
    return bin(x).count("1")

def identity(x):
    return x

def attack_location(x, correct_key, fault_injected = 0):
    if fault_injected:
        # x = (x & 0xfc) | (x & random.randint(0,0x3))
        # x &= random.randint(0,0xfc)
        x &= 0xfe
    y = Sbox[x]
    y ^= correct_key
    return y

def uniform_dist(x):
    if "HW" in ANALYSIS_MODEL:
        return math.comb(n_bits, x) / power_two
    else:
        return 1/power_two

def leak_f(x):
    if "HW" in ANALYSIS_MODEL:
        f = HW
    else:
        f = identity
    return f(x & (power_two - 1))

def get_SEI(key_hyp, list_ineffective, n_ineffective):
    if "HW" in ANALYSIS_MODEL:
        n_leak_val = n_bits + 1
    else:
        n_leak_val = power_two
        
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
    #     print(list_freq[j]/n_ineffective)
    # print(chi)
    # print(n_ineffective)
    # input()
    return chi*n_ineffective


def main():

    for n_enc in range(10, 2010, 10):
        ave_rank = 0
        ave_sei_correct = 0
        ave_sei_wrong_max = 0
        ave_sei_wrong_mu = 0
        ave_n_ineff = 0
        n_rank_1 = 0
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
                sei_correct = SEI_sorted[rank-1][1]
                list_sei = list(dict_SEI.values())
                list_sei.remove(sei_correct)
                sei_wrong_max = max(list_sei)
                sei_wrong_mu = sum(list_sei)/len(list_sei)
            else:
                rank = 128
            ave_rank += rank
            ave_sei_correct += sei_correct
            ave_sei_wrong_max += sei_wrong_max
            ave_sei_wrong_mu += sei_wrong_mu
            ave_n_ineff += n_ineffective
            if rank == 1:
                n_rank_1 += 1
            # print(f'Correct key rank: {rank}')

        ave_rank /= 256
        ave_sei_correct /= 256
        ave_sei_wrong_max /= 256
        ave_sei_wrong_mu /= 256
        ave_n_ineff /= 256
        print(f"\n #{n_enc} Ave. correct key rank = {ave_rank:.1f}, Ave. sei_r = {ave_sei_correct:.1f}, Ave. sei_w_max = {ave_sei_wrong_max:.1f}, "
                f"Ave, sei_w_mu = {ave_sei_wrong_mu:.1f}, Ave. n_ineff = {ave_n_ineff:.1f}, n_rank_1 = {n_rank_1}")

if __name__ == '__main__':
    main()