from aes import Sbox
from tqdm import tqdm
import random, math, itertools, pickle, sys
from scipy import stats
from fire import Fire

random.seed(20)

alpha = 1
beta = 0.5
n_ave_key = 256

def HW(x):
    return bin(x).count("1")

def fault_injection(x, correct_key, fault_injected = 0, n_simulated_fault_bit = 0):
    fault_byte = x ^ correct_key
    fault_byte = Sbox[fault_byte]

    if fault_injected:
        fault_byte = (fault_byte & (256 - 2**n_simulated_fault_bit)) | (fault_byte & random.randint(0,2**n_simulated_fault_bit - 1))
        # fault_byte &= 0x1

    return fault_byte

def get_Score(ANALYSIS_TYPE, key_hyp, list_inef_ef, n_inef_ef):
        
    p_em = [0] * 256
    p_model = [0] * 256
    for x in range(256):
        p_em[x] = list_inef_ef[x] / n_inef_ef
        Z = Sbox[x ^ key_hyp]
        h = HW(Z)
        if ANALYSIS_TYPE == 'inef':
            p_model[x] = (alpha**(1-h))*(beta**h)
        elif ANALYSIS_TYPE == 'ef':
            p_model[x] = 1 - ((alpha**(1-h))*(beta**h))

    KL = stats.entropy(p_em, p_model)
    return KL

    ### Calc SEI
    # sei = 0
    # for i in range(256):
    #     sei += (p_em_inef[i]/ - p_model[i])**2

    # return sei

def main(n_simulated_fault_bit, ANALYSIS_TYPE = "inef"):
    """
    Args:
    n_simulated_fault_bit: [REQUIRED] The number of bits to be fault-injected. [1, 8].
    ANALYSIS_TYPE: One of ["inef", "ef", "hybrid"]
    """
    for n_enc in range(100, 5100, 100):
        ave_rank = 0
        ave_sei_correct = 0
        ave_sei_wrong_min = 0
        ave_sei_wrong_mu = 0
        ave_n_ineff_ef = 0
        n_rank_1 = 0
        for correct_key in range(n_ave_key):
            #print(f"\nCorrect key: {correct_key:x}")
            n_ineffective = 0
            list_freq_ineffective = [0] * 256
            list_freq_effective = [0] * 256
            dict_SEI = {}

            for i in range(n_enc):
                ptxt = random.randint(0, 256 - 1)
                #print(f"{ptxt:x}")
                Z = fault_injection(ptxt, correct_key, fault_injected = 0, n_simulated_fault_bit = n_simulated_fault_bit)
                Zp = fault_injection(ptxt, correct_key, fault_injected = 1, n_simulated_fault_bit = n_simulated_fault_bit)
                rand = random.randint(0, 1)
                if rand != 0:
                    ### 90% miss
                    Zp = Z
                if Z == Zp:
                    # Inneffective
                    list_freq_ineffective[ptxt] += 1
                    n_ineffective += 1
                else:
                    # Effective
                    list_freq_effective[ptxt] += 1
            # print(f'{n_ineffective} ineffective faults out of {n_enc} fault injection ({n_ineffective/n_enc*100} %)')

            if ANALYSIS_TYPE == 'inef':
                n_inef_ef = n_ineffective
                list_inef_ef = list_freq_ineffective
            elif ANALYSIS_TYPE == 'ef':
                n_inef_ef = n_enc - n_ineffective
                list_inef_ef = list_freq_effective

            sei_correct, sei_wrong_min, sei_wrong_mu = 0, 0, 0
            if n_inef_ef > 0:
                for key_hyp in range(256):
                    dict_SEI[hex(key_hyp)] = get_Score(ANALYSIS_TYPE, key_hyp, list_inef_ef, n_inef_ef)
                SEI_sorted = sorted(dict_SEI.items(), key=lambda x:x[1])
                # print(f'Top 10 SEIs: {SEI_sorted[:9]}')

                ### Correct key rank
                rank = SEI_sorted.index((hex(correct_key), dict_SEI[hex(correct_key)])) + 1
                sei_correct = SEI_sorted[rank-1][1]

                list_sei = list(dict_SEI.values())
                list_sei.remove(sei_correct)
                sei_wrong_min = min(list_sei)
                sei_wrong_mu = sum(list_sei)/len(list_sei)

            else:
                rank = 128
            ave_rank += rank
            ave_sei_correct += sei_correct
            ave_sei_wrong_min += sei_wrong_min
            ave_sei_wrong_mu += sei_wrong_mu
            ave_n_ineff_ef += n_inef_ef
            if rank == 1:
                n_rank_1 += 1
            # print(f'Correct key rank: {rank}')

        ave_rank /= n_ave_key
        ave_sei_correct /= n_ave_key
        ave_sei_wrong_min /= n_ave_key
        ave_sei_wrong_mu /= n_ave_key
        ave_n_ineff_ef /= n_ave_key
        # print(f"#{n_enc} Ave. correct key rank = {ave_rank:.1f}, Ave. sei_r = {ave_sei_correct:.1f}, Ave. sei_w_max = {ave_sei_wrong_min:.1f}, "
                # f"Ave, sei_w_mu = {ave_sei_wrong_mu:.1f}, Ave. n_ineff = {ave_n_ineff_ef:.1f}, n_rank_1 = {n_rank_1}")
        print(f"{ave_sei_correct} {ave_sei_wrong_min} {ave_n_ineff_ef}")


if __name__ == '__main__':
    Fire(main)