from aes import Sbox, InvSbox, AES, text2column, column2text, mix_single_column, inv_mix_single_column, sub_bytes_column, inv_sub_bytes_column
from tqdm import tqdm
import random, math, itertools
random.seed(20)

dist_bin = [1, 8, 28, 56, 70, 56, 28, 8, 1]

ANALYSIS_MODEL = "5bits" ### ['n'bits_HW or 'n'bits]
ATTACK_LOCATION = "SB_in" ### ['SB_in' or "MC_in"]
TARGET_BITS = None #(0,1,2,3,4) ### A tuple of 0-7 or None
print(ANALYSIS_MODEL)
n_bits = int(ANALYSIS_MODEL[0])
if not TARGET_BITS is None:
    assert n_bits == len(TARGET_BITS), "The number of model bits and target bits differ"
power_two = 2**n_bits
n_ave_key = 64

def HW(x):
    return bin(x).count("1")

def identity(x):
    return x

def fault_injection(x, correct_key, fault_injected = 0):
    if ATTACK_LOCATION == "MC_in":
        fault_byte = x[3]
    else:
        fault_byte = x

    if fault_injected:
        fault_byte = (fault_byte & 0xe0) | (fault_byte & random.randint(0,0x1f))
        # fault_byte &= random.randint(0,0xff)
        # fault_byte &= 0x1

    if ATTACK_LOCATION == "MC_in":
        y = mix_single_column([x[0], x[1], x[2], fault_byte])
        y[0] ^= 0xde
        y[1] ^= 0xad
        y[2] ^= 0xbe
        y[3] ^= 0xef
        y = sub_bytes_column(y)
        #ShitRows
        y[3] ^= correct_key

    elif ATTACK_LOCATION == "SB_in":
        y = Sbox[fault_byte]
        y ^= correct_key

    return y

def uniform_dist(x):
    if "HW" in ANALYSIS_MODEL:
        return math.comb(n_bits, x) / power_two
    else:
        return 1/power_two

def leak_f(x, _target_bits):
    if "HW" in ANALYSIS_MODEL:
        f = HW
    else:
        f = identity
    
    y = 0
    for bit_pos in _target_bits:
        y <<= 1
        y |= f((x & (2**bit_pos)) >> bit_pos)
    return y

def get_SEI(key_hyp, list_ineffective, n_ineffective):
    if "HW" in ANALYSIS_MODEL:
        n_leak_val = n_bits + 1
    else:
        n_leak_val = power_two
        
    ### Init dictionary
    list_freq = [[0]*n_leak_val for i in range(math.comb(8, n_bits))]

    for ctxt in list_ineffective:
        if ATTACK_LOCATION == "MC_in":
            column = [ctxt[0], ctxt[1], ctxt[2], ctxt[3] ^ key_hyp]
            #ShitRows
            column = inv_sub_bytes_column(column)
            #AddRoundKey
            column = inv_mix_single_column(column)
            t1 = column[3]
        elif ATTACK_LOCATION == "SB_in":
            t0 = ctxt ^ key_hyp
            t1 = InvSbox[t0]
        if TARGET_BITS is None:
            for i, target in enumerate(itertools.combinations([0,1,2,3,4,5,6,7], n_bits)):
                leak = leak_f(t1, target)
                list_freq[i][leak] += 1
        else:
            leak = leak_f(t1, TARGET_BITS)
            list_freq[0][leak] += 1

    ### Calc SEI
    # sei = 0
    # for j in range(n_leak_val):
    #     sei += (list_freq[j]/n_ineffective - uniform_dist(j))**2
    # return sei

    ### Calc CHI
    chi = 0
    if TARGET_BITS is None:
        for i in range(math.comb(8, n_bits)):
            t_chi = 0
            for j in range(n_leak_val):
                t_chi += ((list_freq[i][j]/n_ineffective - uniform_dist(j))**2) / uniform_dist(j)
            chi = max(chi, t_chi)
    else:
        for j in range(n_leak_val):
            chi += ((list_freq[0][j]/n_ineffective - uniform_dist(j))**2) / uniform_dist(j)

    return chi*n_ineffective


def main():

    for n_enc in range(10, 310, 10):
        ave_rank = 0
        ave_sei_correct = 0
        ave_sei_wrong_max = 0
        ave_sei_wrong_mu = 0
        ave_n_ineff = 0
        n_rank_1 = 0
        for correct_key in range(n_ave_key):
            #print(f"\nCorrect key: {correct_key:x}")
            list_ineffective = []
            dict_SEI = {}

            for i in range(n_enc):
                if ATTACK_LOCATION == "MC_in":
                    int_state = [random.randint(0, 256 - 1) for i in range(4)]
                elif ATTACK_LOCATION == "SB_in":
                    int_state = random.randint(0, 256 - 1)
                #print(f"{ptxt:x}")
                C = fault_injection(int_state, correct_key, fault_injected = 0)
                Cp = fault_injection(int_state, correct_key, fault_injected = 1)
                if C == Cp:
                    # ineffective
                    list_ineffective.append(Cp)
            n_ineffective = len(list_ineffective)
            # print(f'{n_ineffective} ineffective faults out of {n_enc} fault injection ({n_ineffective/n_enc*100} %)')

            sei_correct, sei_wrong_max, sei_wrong_mu = 0, 0, 0
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

        ave_rank /= n_ave_key
        ave_sei_correct /= n_ave_key
        ave_sei_wrong_max /= n_ave_key
        ave_sei_wrong_mu /= n_ave_key
        ave_n_ineff /= n_ave_key
        # print(f"#{n_enc} Ave. correct key rank = {ave_rank:.1f}, Ave. sei_r = {ave_sei_correct:.1f}, Ave. sei_w_max = {ave_sei_wrong_max:.1f}, "
                # f"Ave, sei_w_mu = {ave_sei_wrong_mu:.1f}, Ave. n_ineff = {ave_n_ineff:.1f}, n_rank_1 = {n_rank_1}")
        print(f"{ave_sei_correct},{ave_sei_wrong_max},{ave_sei_wrong_mu}")

if __name__ == '__main__':
    main()