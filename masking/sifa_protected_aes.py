from aes_sbox import *
from toffoli import *
import random

def s_sc_4(a: GF2_22, b: GF2_22, c: GF2_22):
    t0 = b + c
    a = a + t0.sqr_scale()
    return a, b, c

def s_sc_2(a: GF2_2, b: GF2_2, c: GF2_2):
    t0 = b + c
    a = a + t0.sqr_scale2()
    return a, b, c

def main():

    ### Constraint generation
    a0 = GF2_22(fromint = random.randint(0, 2**4 - 1))
    a1 = a0
    b0 = GF2_2(fromint = random.randint(0, 2**2 - 1))
    b1 = b0
    c0 = GF2_22(fromint = random.randint(0, 2**4 - 1))
    c1 = c0
    d0 = GF2_222(fromint = random.randint(0, 2**8 - 1))
    d1 = d0

    ### Input generation
    tv = random.randint(0, 255)
    X = GF2_8(fromint = tv)
    X_222 = AES_map.to_GF2_222(X)
    mask = random.randint(0, 255)
    x0 = GF2_8(fromint =  mask)
    x1 = X + x0

    # Isomorphism
    x0 = AES_map.to_GF2_222(x0)
    x1 = AES_map.to_GF2_222(x1)

    # Composite field inversion on the Canright's normal basis
    a0, a1, x0.coeff[1], x1.coeff[1], x0.coeff[0], x1.coeff[0] = pTS_4(a0, a1, x0[1], x1[1], x0[0], x1[0])  # GF2_22 multiplication
    a0, x0.coeff[1], x0.coeff[0] = s_sc_4(a0, x0[1], x0[0]) # GF2_22 square scaling with accumulation
    a1, x1.coeff[1], x1.coeff[0] = s_sc_4(a1, x1[1], x1[0]) # GF2_22 square scaling with accumulation

    b0, b1, a0.coeff[1], a1.coeff[1], a0.coeff[0], a1.coeff[0] = pTS_2(b0, b1, a0[1], a1[1], a0[0], a1[0])  # GF2_2 multiplication
    b0, a0.coeff[1], a0.coeff[0] = s_sc_2(b0, a0[1], a0[0]) # GF2_2 square scaling with accumulation
    b1, a1.coeff[1], a1.coeff[0] = s_sc_2(b1, a1[1], a1[0]) # GF2_2 square scaling with accumulation

    b0 = b0.inv()   # Bit swap
    b1 = b1.inv()   # Bit swap
    print(b0 + b1)
    X_222.inv()



if __name__ == "__main__":
    main()