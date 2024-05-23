from aes_sbox import *
from toffoli import *
from copy import deepcopy
import random

def s_sc_4(a: GF2_22, b: GF2_22, c: GF2_22):
    t0 = b + c
    a = a + t0.sqr_scale()
    return a, b, c

def s_sc_2(a: GF2_2, b: GF2_2, c: GF2_2):
    t0 = b + c
    a = a + t0.sqr_scale2()
    return a, b, c

def clone(x):
    return deepcopy(x), x

def masked_sbox_v1(x0, x1, a0, a1, b0, b1, c0, c1, d0, d1):
    ### Daemen's (8.a) construction with constraints.

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

    c0.coeff[1], c1.coeff[1], a0.coeff[0], a1.coeff[0], b0, b1 = pTS_2(c0[1], c1[1], a0[0], a1[0], b0, b1)  # GF2_2 multiplication
    c0.coeff[0], c1.coeff[0], a0.coeff[1], a1.coeff[1], b0, b1 = pTS_2(c0[0], c1[0], a0[1], a1[1], b0, b1)  # GF2_2 multiplication

    d0.coeff[1], d1.coeff[1], x0.coeff[0], x1.coeff[0], c0, c1 = pTS_4(d0[1], d1[1], x0[0], x1[0], c0, c1)  # GF2_22 multiplication
    d0.coeff[0], d1.coeff[0], x0.coeff[1], x1.coeff[1], c0, c1 = pTS_4(d0[0], d1[0], x0[1], x1[1], c0, c1)  # GF2_22 multiplication

    d0 = AES_map.to_GF2_8(d0)
    d1 = AES_map.to_GF2_8(d1)

    # Add constant
    const = GF2_8(fromint = 0x63)
    d0 = d0 + const

    return x0, x1, a0, a1, b0, b1, c0, c1, d0, d1

def masked_sbox_v2(x0, x1, a0, b0, c0, d0):
    ### Daemen's (8.b) construction with cloning.

    # Cloning
    a1, a0 = clone(a0)
    b1, b0 = clone(b0)
    c1, c0 = clone(c0)
    d1, d0 = clone(d0)

    e0, e1, f0, f1, g0, g1, h0, h1, y0, y1 = masked_sbox_v1(x0, x1, a0, a1, b0, b1, c0, c1, d0, d1)

    return y0, y1, f0, g0, h0, e0

def main():

    ### Constraint generation
    a0 = GF2_22(fromint = random.randint(0, 2**4 - 1))
    a1 = deepcopy(a0)
    b0 = GF2_2(fromint = random.randint(0, 2**2 - 1))
    b1 = deepcopy(b0)
    c0 = GF2_22(fromint = random.randint(0, 2**4 - 1))
    c1 = deepcopy(c0)
    d0 = GF2_222(fromint = random.randint(0, 2**8 - 1))
    d1 = deepcopy(d0)

    ### Input generation
    tv = random.randint(0, 255)
    X = GF2_8(fromint = tv)
    X_222 = AES_map.to_GF2_222(X)
    mask = random.randint(0, 255)
    x0 = GF2_8(fromint =  mask)
    x1 = X + x0

    e0, e1, f0, f1, g0, g1, h0, h1, y0, y1 = masked_sbox_v1(x0, x1, a0, a1, b0, b1, c0, c1, d0, d1)
    print(f'v1:  {hex((y0+y1).toInt())}')

    y0, y1, f0, g0, h0, e0 = masked_sbox_v2(x0, x1, a0, b0, c0, d0)
    print(f'v2:  {hex((y0+y1).toInt())}')

    print(f'ANS: {hex(AES_map.Sbox[tv])}')

if __name__ == "__main__":
    main()