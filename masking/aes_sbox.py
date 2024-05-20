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
    N2PAffine = matReduc(Affine@N2P)

    def to_GF2_222(x: GF2_8) -> GF2_222:
        ### Base transform.
        binArray = x.toBinArray()
        a = vecReduc(AES_map.P2N@binArray)
        return GF2_222(GF2_22(GF2_2(GF2(a[0]), GF2(a[1])), GF2_2(GF2(a[2]), GF2(a[3]))), GF2_22(GF2_2(GF2(a[4]), GF2(a[5])), GF2_2(GF2(a[6]), GF2(a[7]))))

    def to_GF2_8_A(x: GF2_222) -> GF2_8:
        ### Base transform with Affine transform.
        binArray = x.toBinArray()
        e = vecReduc(AES_map.N2PAffine@binArray)
        e = e ^ [1,1,0,0,0,1,1,0]
        return GF2_8(e[0],e[1],e[2],e[3],e[4],e[5],e[6],e[7])

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

    def scale(self):
        ### times alpha
        return GF2_2(self[1], self[1] + self[0])

    def scale2(self):
        ### times alpha^2
        return GF2_2(self[1] + self[0], self[0])

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
        t0 = (self[1] + self[0]).sqr()
        t1 = t0.scale2()
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

    def inv(self):
        t0 = self[0] + self[1]
        #square_scale = GF2_2(t0[0], t0[0] + t0[1])
        square_scale = t0.sqr().scale2()
        power5 = square_scale + self[0]*self[1]
        inv = power5.sqr()
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
        square_scale = t0.sqr().scale()
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