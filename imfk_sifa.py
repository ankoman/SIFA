from aes import Sbox
import csv
import random, math, itertools, pickle, sys
from scipy import stats
from fire import Fire
import numpy as np

random.seed(20)

n_ave_key = 256

def HW(x):
    return bin(x).count("1")

def fault_injection(x, correct_key, alpha, beta):
    fault_byte = x ^ correct_key
    fault_byte = Sbox[fault_byte]

    h = HW(fault_byte)
    inef_rate = (alpha**(8-h))*(beta**h)
    r = random.random()

    is_inef = False
    if r < inef_rate:
        is_inef = True

    return is_inef

def get_Score(ANALYSIS_TYPE, key_hyp, list_inef_ef, n_inef_ef, alpha, beta):
        
    p_em = []
    p_model = []
    for x in range(256):
        Z = Sbox[x ^ key_hyp]
        h = HW(Z)

        if ANALYSIS_TYPE == 'ef':
            p_model.append(1 - ((alpha**(8-h))*(beta**h)))
        else:
            p_model.append((alpha**(8-h))*(beta**h))

        ### Naive p_em calculation. Be 0 when no inef occurs
        p_em.append(list_inef_ef[x] / n_inef_ef[x] if n_inef_ef[x] != 0 else p_model[-1])

        ### p_em calculation with no probability assignment when no inef occurs
        # if list_inef_ef[x] != 0:
        #     p_em.append(list_inef_ef[x] / n_inef_ef)
        # else:
        #     p_model.pop()

        # ## p_em calculation with model probability assignment when no inef occurs
        # if list_inef_ef[x] != 0:
        #     p_em.append(list_inef_ef[x] / n_inef_ef)
        # else:
        #     p_em.append(p_model[-1])

    KL = stats.entropy(p_em, p_model)
    return KL

    ### Calc SEI
    # sei = 0
    # for i in range(256):
    #     sei += (p_em_inef[i]/ - p_model[i])**2

    # return sei

def main(alpha_act, beta_act, alpha_hyp, beta_hyp, ANALYSIS_TYPE = "inef", ):
    """
    Args:
    alpha_act: Actual fault parameter alpha
    beta_act:  Actual fault parameter beta
    alpha_hyp: Hypothesised alpha to be used for analysis 
    beta_hyp:  Hypothesised beta to be used for analysis 
    ANALYSIS_TYPE: One of ["inef", "ef", "inef_all_x"] (Default: inef)
    """

    list_res = []
    for n_enc in [250, 260, 50, 60, 70, 80, 90, 100, 200, 300, 400, 500, 1000, 2000, 3000, 4000, 5000, 10000, 20000, 30000, 40000, 50000, 100000]: #range(10, 510, 10):
        ave_rank = 0
        ave_sei_correct = 0
        ave_sei_wrong_min = 0
        ave_sei_wrong_mu = 0
        ave_n_ineff_ef = 0
        n_rank_1 = 0
        for correct_key in range(n_ave_key):
            #print(f"\nCorrect key: {correct_key:x}")
            n_ineffective = 0
            list_freq_ineffective = np.array([0] * 256)
            list_freq_effective = np.array([0] * 256)
            dict_SEI = {}

            for i in range(n_enc):
                ptxt = random.randint(0, 256 - 1)
                #print(f"{ptxt:x}")
                is_inef = fault_injection(ptxt, correct_key, alpha_act, beta_act)

                # rand = random.randint(0, 1)
                # if rand != 0:
                #     ### 90% miss
                #     Zp = Z

                if is_inef:
                    # Inneffective
                    list_freq_ineffective[ptxt] += 1
                    n_ineffective += 1
                else:
                    # Effective
                    list_freq_effective[ptxt] += 1
            # print(f'{n_ineffective} ineffective faults out of {n_enc} fault injection ({n_ineffective/n_enc*100} %)')

            if ANALYSIS_TYPE == 'inef':
                n_inef_ef = n_ineffective
                list_n_inef_ef = [n_ineffective] * 256
                list_inef_ef = list_freq_ineffective
            elif ANALYSIS_TYPE == 'ef':
                n_inef_ef = n_enc - n_ineffective
                list_n_inef_ef = [n_enc - n_ineffective] * 256
                list_inef_ef = list_freq_effective
            elif ANALYSIS_TYPE == 'inef_all_x':
                n_inef_ef = n_ineffective
                list_n_inef_ef = list_freq_ineffective + list_freq_effective
                list_inef_ef = list_freq_ineffective

            sei_correct, sei_wrong_min, sei_wrong_mu = 0, 0, 0
            if n_inef_ef > 0:
                for key_hyp in range(256):
                    dict_SEI[hex(key_hyp)] = get_Score(ANALYSIS_TYPE, key_hyp, list_inef_ef, list_n_inef_ef, alpha_hyp, beta_hyp)
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

        attacked = ave_sei_correct < ave_sei_wrong_min
        list_res.append([n_enc, ave_sei_correct, ave_sei_wrong_min, ave_n_ineff_ef, ave_rank, attacked])


    with open(f"res/{ANALYSIS_TYPE}-a_act{alpha_act}-b_act{beta_act}-a_hyp{alpha_hyp}-b_hyp{beta_hyp}.csv", 'w', encoding='utf-8')as f:
        writer = csv.writer(f,lineterminator='\n')
        writer.writerows(list_res)
 
if __name__ == '__main__':
    Fire(main)