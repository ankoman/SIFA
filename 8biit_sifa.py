from aes import Sbox, InvSbox
from tqdm import tqdm
import random

dist_bin = [1, 8, 28, 56, 70, 56, 28, 8, 1]

ATTACK_MODEL = "HW"
correct_key = 0x7e#random.randint(0, 255)
print(f"Correct key: {correct_key:x}")

def attack_location(x, fault_injected = 0):
    if fault_injected:
        x &= random.randint(0, 255)
    y = Sbox[x]
    y ^= correct_key
    return y

def uniform_dist(x):
    if ATTACK_MODEL == "HW":
        return dist_bin[x] / 256

def leak_f(x):
    if ATTACK_MODEL == "HW":
        return bin(x).count("1")

def get_SEI(key_hyp, list_ineffective, n_ineffective):
    if ATTACK_MODEL == "HW":
        n_leak_val = 9

    ### Init dictionary
    list_freq = [0]*n_leak_val

    for ctxt in list_ineffective:
        t0 = ctxt ^ key_hyp
        t1 = InvSbox[t0]
        leak = leak_f(t1)
        list_freq[leak] += 1

    ### Calc SEI
    sei = 0
    for j in range(n_leak_val):
        sei += (list_freq[j]/n_ineffective - uniform_dist(j))**2
    return sei

def main():
    list_ineffective = []
    dict_SEI = {}

    n_enc = 100
    for i in range(n_enc):
        int_state = random.randint(0, 256 - 1)
        #print(f"{ptxt:x}")
        C = attack_location(int_state, fault_injected = 0)
        Cp = attack_location(int_state, fault_injected = 1)
        if C == Cp:
            # ineffective
            list_ineffective.append(Cp)
    n_ineffective = len(list_ineffective)
    print(f'{n_ineffective} ineffective faults out of {n_enc} fault injection ({n_ineffective/n_enc*100} %)')

    for key_hyp in range(256):
        dict_SEI[hex(key_hyp)] = get_SEI(key_hyp, list_ineffective, n_ineffective)
    SEI_sorted = sorted(dict_SEI.items(), key=lambda x:x[1])[::-1]
    print(f'Top 10 SEIs: {SEI_sorted[:9]}')

    ### Correct key SEI
    print(f'Correct key rank: {SEI_sorted.index((hex(correct_key), dict_SEI[hex(correct_key)])) + 1}')


if __name__ == '__main__':
    main()