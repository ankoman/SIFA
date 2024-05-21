from aes_sbox import *
import random

def s_sc_4(a: GF2_22, b: GF2_22, c: GF2_22):
    t0 = b + c
    a = a + t0.sqr_scale()
    return a, b, c

def s_sc_2(a: GF2_2, b: GF2_2, c: GF2_2):
    t0 = b + c
    a = a + t0.sqr_scale()
    return a, b, c

def main():

    ### Constraint generation
    a0 = random.randint(0, 255)
    a0 = a1
    b0 = random.randint(0, 255)
    b0 = b1
    c0 = random.randint(0, 255)
    c0 = c1
    d0 = random.randint(0, 255)
    d0 = d1

    ### Input generation
    tv = 0x12
    mask = random.randint(0, 255)
    x0 = GF2_8(fromint = tv ^ mask)
    x1 = GF2_8(fromint = mask)

    x0 = AES_map.to_GF2_222(x0)
    x1 = AES_map.to_GF2_222(x1)
    x0_H, x0_L = x0[1], x0[0]
    x1_H, x1_L = x1[1], x1[0]

    a0, a1, b0, b1, c0, c1 = pTS_4(a0, a1, x0_H, x1_H, x0_L, x1_L)



if __name__ == "__main__":
    main()