import random
from aes_sbox import GF2_22, GF2_2

def toffoli(a: bool, b: bool, c: bool):
    return a ^ (b & c), b, c

def masked_toffoli(a0: bool, a1: bool, b0: bool, b1: bool, c0: bool, c1: bool):
    a0, b0, c1 = toffoli(a0, b0, c1)
    a0, b0, c0 = toffoli(a0, b0, c0)
    a1, b1, c1 = toffoli(a1, b1, c1)
    a1, b1, c0 = toffoli(a1, b1, c0)
    return a0, a1, b0, b1, c0, c1

def pT_4(a: GF2_22, b: GF2_22, c: GF2_22) -> [GF2_22, GF2_22, GF2_22]:
    return a + (b * c), b, c

def pTS_4(a0: GF2_22, a1: GF2_22, b0: GF2_22, b1: GF2_22, c0: GF2_22, c1: GF2_22):
    a0, b0, c1 = pT_4(a0, b0, c1)
    a0, b0, c0 = pT_4(a0, b0, c0)
    a1, b1, c1 = pT_4(a1, b1, c1)
    a1, b1, c0 = pT_4(a1, b1, c0)
    return a0, a1, b0, b1, c0, c1

def pT_2(a: GF2_2, b: GF2_2, c: GF2_2) -> [GF2_2, GF2_2, GF2_2]:
    return a + (b * c), b, c

def pTS_2(a0: GF2_2, a1: GF2_2, b0: GF2_2, b1: GF2_2, c0: GF2_2, c1: GF2_2):
    a0, b0, c1 = pT_2(a0, b0, c1)
    a0, b0, c0 = pT_2(a0, b0, c0)
    a1, b1, c1 = pT_2(a1, b1, c1)
    a1, b1, c0 = pT_2(a1, b1, c0)
    return a0, a1, b0, b1, c0, c1

def main():
    print('Toffoli test')
    for i in range(8):
        c = i & 1
        b = (i >> 1) & 1
        a = (i >> 2) & 1
        print(f'{a, b, c} -> {toffoli(a, b, c)}')

    print('\nMasked toffoli test')
    for i in range(8):
        r = random.randint(0, 7)
        s = i ^ r
        c0 = s & 1
        b0 = (s >> 1) & 1
        a0 = (s >> 2) & 1
        c1 = r & 1
        b1 = (r >> 1) & 1
        a1 = (r >> 2) & 1

        a0, a1, b0, b1, c0, c1 = masked_toffoli(a0, a1, b0, b1, c0, c1)

        print(f'{a0^a1, b0^b1, c0^c1}')

    print('\npT_2 test')
    for i in range(4*4*4):
        c = GF2_2(fromint = i & 0x3)
        b = GF2_2(fromint = (i >> 2) & 0x3)
        a = GF2_2(fromint = (i >> 4) & 0x3)
        print(f'{a, b, c} -> {pT_2(a, b, c)}')

if __name__ == "__main__":
    main()