from __future__ import annotations
import numpy as np

### Vector values are represented as a binary array
### A vector X is represented as x^3 x^2 x^1 x^0 in the Daemen's work
### In this implementation, a vector is a list. 
### For X = [x0, x1], X[0] is the LSB. Higher degree term on the right.
### But for simplisity, vectors are shown in reverse order (higher degree on the left).

def matReduc(mat):
    reduced = []
    for row in mat:
        r = []
        for elem in row:
            r.append(int(elem % 2))
        reduced.append(r)
    return np.array(reduced)

def vecReduc(vec):
    reduced = []
    for elem in vec:
        reduced.append(int(elem % 2))
    return np.array(reduced)


class AES_map:
    Sbox = (
        0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
        0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
        0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
        0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
        0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
        0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
        0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
        0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
        0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
        0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
        0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
        0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
        0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
        0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
        0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
        0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16
        )
    # ### Normal bases GF(2_222) to polynomial basis GF(2_8). Upper is the MSB
    # N2P = np.array([
    #     [0,0,0,1,0,0,1,0],
    #     [1,1,1,0,1,0,1,1],
    #     [1,1,1,0,1,1,0,1],
    #     [0,1,0,0,0,0,1,0],
    #     [0,1,1,1,1,1,1,0],
    #     [1,0,1,1,0,0,1,0],
    #     [0,0,1,0,0,0,1,0],
    #     [0,0,0,0,0,1,0,0]])

    # ### AES Affine transform. Upper is the MSB
    # Affine = np.array([
    #     [1,1,1,1,1,0,0,0],
    #     [0,1,1,1,1,1,0,0],
    #     [0,0,1,1,1,1,1,0],
    #     [0,0,0,1,1,1,1,1],
    #     [1,0,0,0,1,1,1,1],
    #     [1,1,0,0,0,1,1,1],
    #     [1,1,1,0,0,0,1,1],
    #     [1,1,1,1,0,0,0,1]])

    ### Normal bases GF(2_222) to polynomial basis GF(2_8). Lower is the MSB
    N2P = np.array([
        [0,0,1,0,0,0,0,0],
        [0,1,0,0,0,1,0,0],
        [0,1,0,0,1,1,0,1],
        [0,1,1,1,1,1,1,0],
        [0,1,0,0,0,0,1,0],
        [1,0,1,1,0,1,1,1],
        [1,1,0,1,0,1,1,1],
        [0,1,0,0,1,0,0,0]
        ])

    ### AES Affine transform. Lower is the MSB
    Affine = np.array([
        [1,0,0,0,1,1,1,1],
        [1,1,0,0,0,1,1,1],
        [1,1,1,0,0,0,1,1],
        [1,1,1,1,0,0,0,1],
        [1,1,1,1,1,0,0,0],
        [0,1,1,1,1,1,0,0],
        [0,0,1,1,1,1,1,0],
        [0,0,0,1,1,1,1,1]])

    P2N = matReduc(np.linalg.inv(N2P))
    # [[1 1 1 1 0 0 1 0]
    #  [1 0 0 0 0 1 1 0]
    #  [1 0 0 0 0 0 0 0]
    #  [1 1 0 1 1 0 0 1]
    #  [1 0 0 0 0 1 1 1]
    #  [1 1 0 0 0 1 1 0]
    #  [1 0 0 0 1 1 1 0]
    #  [1 1 1 0 0 1 1 1]]

    N2PAffine = matReduc(Affine@N2P)
    # [[0 1 0 0 1 0 1 0]
    #  [0 1 0 0 1 1 0 0]
    #  [1 0 1 1 0 1 1 0]
    #  [0 0 0 1 1 1 1 1]
    #  [0 0 0 1 0 1 0 1]
    #  [1 0 0 0 0 0 1 0]
    #  [0 0 0 1 0 0 0 1]
    #  [0 0 0 1 0 1 0 0]]

    def to_GF2_222(x: GF2_8) -> GF2_222:
        ### Base transform.
        binArray = x.toBinArray()
        a = vecReduc(AES_map.P2N@binArray)
        return GF2_222(GF2_22(GF2_2(GF2(a[0]), GF2(a[1])), GF2_2(GF2(a[2]), GF2(a[3]))), GF2_22(GF2_2(GF2(a[4]), GF2(a[5])), GF2_2(GF2(a[6]), GF2(a[7]))))

    def to_GF2_8(x: GF2_222) -> GF2_8:
        ### Base transform with Affine transform.
        binArray = x.toBinArray()
        e = vecReduc(AES_map.N2PAffine@binArray)
        return GF2_8(GF2(e[0]),GF2(e[1]),GF2(e[2]),GF2(e[3]),GF2(e[4]),GF2(e[5]),GF2(e[6]),GF2(e[7]))

    def to_GF2_8_A(x: GF2_222) -> GF2_8:
        ### Base transform with Affine transform.
        binArray = x.toBinArray()
        e = vecReduc(AES_map.N2PAffine@binArray)
        e = e ^ [1,1,0,0,0,1,1,0]
        return GF2_8(GF2(e[0]),GF2(e[1]),GF2(e[2]),GF2(e[3]),GF2(e[4]),GF2(e[5]),GF2(e[6]),GF2(e[7]))

class GF2:
    def __init__(self, val: bool = 0):
        assert val in [0, 1], f"GF2 constractor failed"
        self.val = val

    def __repr__(self):
        return str(self.val)

    def __str__(self):
        return str(self.val)

    def __add__(self, other):
        return GF2(self.val ^ other.val)

    def __mul__(self, other):
        return GF2(self.val & other.val)

class GF2_2:
    """
    Name:        GF2_2
    A list of two GF2 elements, [x0, x1]. [alpha, alpha^2] is the basis
    x1 is the MSB. Normal basis representation.
    """
    def __init__(self, elem0: GF2 = GF2(), elem1: GF2 = GF2(), fromint: int = None):
        if fromint is None:
            self.coeff = [elem0, elem1]
        else:
            assert fromint < 4, 'GF2_2 elemant bigger than 3.'
            tmp = format(fromint, f'02b')
            self.coeff = [GF2(int(x)) for x in list(tmp)]

    def sqr(self):
        return GF2_2(self[1], self[0])

    def inv(self):
        return self.sqr()

    def scale(self):
        ### times alpha
        return GF2_2(self[1], self[1] + self[0])

    def sqr_scale(self):
        return GF2_2(self[0], self[1] + self[0])

    def scale2(self):
        ### times alpha^2
        return GF2_2(self[1] + self[0], self[0])

    def sqr_scale2(self):
        return GF2_2(self[1] + self[0], self[1])

    def __getitem__(self, index):
        return self.coeff[index]

    def __repr__(self):
        return str(self.coeff)

    def __add__(self, other):
        return GF2_2(self[0] + other[0], self[1] + other[1])

    def __mul__(self, other):
        t = (self[1] + self[0]) * (other[1] + other[0])
        c1 = t + (self[1] * other[1])
        c0 = t + (self[0] * other[0])
        return GF2_2(c0, c1)

class GF2_22:
    """
    Name:        GF2_22
    A list of two GF2_2 elements [x0, x1], x1 and x0 are in GF2_2.
    X in GF2_22 is represented as x0*beta + x1*beta^4, [beta, beta^4] is the normal basis.
    x1 is the MSB. Normal basis representation.
    """
    def __init__(self, elem0: GF2_2 = GF2_2(), elem1: GF2_2 = GF2_2(), fromint: int = None):
        if fromint is None:
            self.coeff = [elem0, elem1]
        else:
            assert fromint < 16, 'GF2_22 elemant bigger than 15.'
            tmp = format(fromint, f'04b')
            x0 = fromint & 0x3
            x1 = fromint >> 2
            self.coeff = [GF2_2(fromint = x0), GF2_2(fromint = x1)]

    def frob(self):
        ### Frobenius map power to 4.
        return GF2_22(self[1], self[0])

    def sqr(self):
        t0 = (self[1] + self[0])
        t1 = t0.sqr_scale2()
        c1 = t1 + self[1].sqr()
        c0 = t1 + self[0].sqr()
        return GF2_22(c0, c1)

    def scale(self):
        # ### times alpha^2beta for Nogami's construction
        # t0 = self[1] + self[0]
        # t1 = t0.scale()
        # c0 = self[0] + t1
        # c1 = t1
        # c0 = c0.scale2()
        # c1 = c1.scale2()

        ### times N^2Z for Canright's construction
        t0 = self[1] + self[0]
        c0 = self[0].scale() + t0
        c1 = t0

        return GF2_22(c0, c1)

    def sqr_scale(self):
        t0 = self[1] + self[0]
        return GF2_22(self[0].sqr_scale(), t0.sqr())

    def inv(self):
        t0 = self[0] + self[1]
        #square_scale = GF2_2(t0[0], t0[0] + t0[1])
        square_scale = t0.sqr_scale2()
        power5 = square_scale + self[0]*self[1]
        inv = power5.inv()
        return GF2_22(inv * self[1], inv * self[0])

    def __getitem__(self, index):
        return self.coeff[index]

    def __repr__(self):
        return str(self.coeff)

    def __add__(self, other):
        return GF2_22(self[0] + other[0], self[1] + other[1])

    def __mul__(self, other):
        ### Higher (H) is 1, lower (L) is 0.
        t0 = (self[1] + self[0]) * (other[0] + other[1])
        t1 = t0.scale2()
        c1 = t1 + (self[1] * other[1])
        c0 = t1 + (self[0] * other[0])
        return GF2_22(c0, c1)

class GF2_222:
    """
    Name:        GF2_222
    A list of two GF2_22 elements [x0, x1], x1 and x0 are in GF2_22.
    X in GF2_222 is represented as x0*gamma + x1*gamma^16, [gamma, gamma^16] is the normal basis.
    x1 is the MSB. Normal basis representation.
    """
    def __init__(self, elem0: GF2_22 = GF2_22(), elem1: GF2_22 = GF2_22(), fromint: int = None):
        if fromint is None:
            self.coeff = [elem0, elem1]
        else:
            assert fromint < 256, 'GF2_222 elemant bigger than 255.'
            tmp = format(fromint, f'08b')
            x0 = fromint & 0xf
            x1 = fromint >> 4
            self.coeff = [GF2_22(fromint = x0), GF2_22(fromint = x1)]

    def inv(self):
        t0 = self[0] + self[1]
        square_scale = t0.sqr_scale()
        power17 = square_scale + self[0]*self[1]
        inv = power17.inv()
        return GF2_222(inv * self[1], inv * self[0])

    def inv_flt(self):
        ### Fermat's little theorem inversion
        a = self
        for i in range(256 - 3):
            a = a * self
        return a

    def __getitem__(self, index):
        return self.coeff[index]

    def __repr__(self):
        return str(self.coeff)

    def __add__(self, other):
        return GF2_222(self[0] + other[0], self[1] + other[1])

    def __mul__(self, other):
        t0 = (self[1] + self[0]) * (other[0] + other[1])
        t1 = t0.scale()
        c1 = t1 + (self[1] * other[1])
        c0 = t1 + (self[0] * other[0])
        return GF2_222(c0, c1)

    def toBinArray(self):
        return [self[0][0][0].val, self[0][0][1].val, self[0][1][0].val, self[0][1][1].val, \
                self[1][0][0].val, self[1][0][1].val, self[1][1][0].val, self[1][1][1].val]

class GF2_8:
    """
    Name:        GF2_8
    A list of eight GF2 elements [x0, x1, x2,...x7], x1 and x0 are in GF2_22.
    X in GF2_8 is represented as x0 + x1*A + x2*A^2,..., x7*A^7, [1, A, A^2, ..., A^7] is the polynomial basis.
    x7 is the MSB. Polynomial basis representation.
    """
    def __init__(self, elem0: GF2 = GF2(), elem1: GF2 = GF2(), elem2: GF2 = GF2(), elem3: GF2 = GF2(), \
                elem4: GF2 = GF2(), elem5: GF2 = GF2(), elem6: GF2 = GF2(), elem7: GF2 = GF2(), fromint: int = None):
        if fromint is None:
            self.coeff = [elem0, elem1, elem2, elem3, elem4, elem5, elem6, elem7]
        else:
            assert fromint < 256, 'GF2_8 elemant bigger than 255.'
            x0 = fromint & 1
            x1 = (fromint >> 1) & 1
            x2 = (fromint >> 2) & 1
            x3 = (fromint >> 3) & 1
            x4 = (fromint >> 4) & 1
            x5 = (fromint >> 5) & 1
            x6 = (fromint >> 6) & 1
            x7 = (fromint >> 7) & 1

            self.coeff = [GF2(x0), GF2(x1), GF2(x2), GF2(x3), GF2(x4), GF2(x5), GF2(x6), GF2(x7)]

    def __getitem__(self, index):
        return self.coeff[index]

    def __repr__(self):
        return str(self.coeff)

    def __add__(self, other):
        return GF2_8(self[0] + other[0], self[1] + other[1], self[2] + other[2], self[3] + other[3],\
                    self[4] + other[4], self[5] + other[5], self[6] + other[6], self[7] + other[7])

    def __mul__(self, other):
        ### Multiplication on a polynomial basis.
        ### Irreducible polynomial q(x) = x^8 + x^4 + x^3 + x + 1

        t = [GF2()] * 15
        for i in range(8):
            for j in range(8):
                t[j+i] = t[j+i] + (other[i] * self[j])

        one = GF2(1)
        for i in range(14, 7, -1):
            if t[i].val == 1:
                t[i-4] = t[i-4] + one
                t[i-5] = t[i-5] + one
                t[i-7] = t[i-7] + one
                t[i-8] = t[i-8] + one
        
        return GF2_8(t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7])

    def inv_flt(self):
        ### Fermat's little theorem inversion
        a = self
        for i in range(256 - 3):
            a = a * self
        return a

    def toInt(self):
        return int("".join(list(reversed(list(map(str, self.coeff))))), 2)
        
    def toBinArray(self):
        return [self[0].val, self[1].val, self[2].val, self[3].val, \
                self[4].val, self[5].val, self[6].val, self[7].val]   


def main():

    print("Test GF2_2_mul, (1, 1) is the unity")
    for i in range(4):
        for j in range(4):
            a = GF2_2(fromint = i)
            b = GF2_2(fromint = j)
            c = a * b
            print(f'{i, j}: {a} * {b} -> {c}')

    print("\nTest GF2_22_mul, (1, 1, 1, 1) is the unity")
    for i in range(16):
        for j in range(16):
            a = GF2_22(fromint = i)
            b = GF2_22(fromint = j)
            c = a * b
            print(f'{i:>2}, {j:>2}: {a} * {b} -> {c}')

    print("\nTest GF2_22 frobenius and mul.")
    for i in range(16):
        a = GF2_22(fromint = i)
        c = a.frob()
        print(f'{i:>2}^4: {a}^4 -> {c} == {a * a * a * a} ?')

    print("\nTest GF2_22 power to 5, which must be in GF(2_2) (the two elements are the same).")
    for i in range(16):
        a = GF2_22(fromint = i)
        print(f'{a * a * a * a * a}')

    print("\nTest GF2_22_inv")
    for i in range(16):
        a = GF2_22(fromint = i)
        a_inv = a.inv()
        print(f'{a} * {a_inv} -> {a * a_inv}')

    print("\nTest GF2_222_inv. (1, 1, 1, 1, 1, 1, 1, 1) is the unity")
    for i in range(256):
        a = GF2_222(fromint = i)
        a_inv = a.inv()
        #print(f'{power17} == {a * a * a * a * a * a * a * a * a * a * a * a * a * a * a * a * a} ?')
        print(f'{a} * {a_inv} -> {a * a_inv}')
        #print(f'{a.inv_flt()} == {a_inv} ?')

    ### Base tranform vectors
    y = GF2_8(fromint = 0xff)
    z = GF2_8(fromint = 0x5c)
    w = GF2_8(fromint = 0xbd)
    N = GF2_8(fromint = 0xbc)

    #print(hex((y*z*w).toInt()))

    ### AES Sbox
    print("\nTest AES Sbox.")
    for i in range(16):
        for j in range(16):
            sbox_in = i*16+j
            sin2_8 = GF2_8(fromint = sbox_in)
            sin2_222 = AES_map.to_GF2_222(sin2_8)
            inv = sin2_222.inv()
            sout2_8 = AES_map.to_GF2_8_A(inv)
            sbox_out = sout2_8.toInt()
            print(f'0x{sbox_out:02x}, ', end = '')
        print()

if __name__ == "__main__":
    main()