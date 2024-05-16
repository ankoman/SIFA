from __future__ import annotations

### Vector values are represented as a binary array
### A vector X is represented as x^3 x^2 x^1 x^0 in the Daemen's work
### In this implementation, a vector is a list. 
### For X = [x0, x1], X[0] is the LSB. Higher degree term on the right.
### But for simplisity, vectors are shown in reverse order (higher degree on the left).

class GF2:
    def __init__(self, val: bool = 0):
        assert val in [0, 1], f"GF2 constractor failed"
        self.val = val

    def __repr__(self):
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
        t1 = t0.scale()
        c1 = t1 + self[1].sqr()
        c0 = t1 + self[0].sqr()
        return GF2_22(c0, c1)

    def scale(self):
        ### times alpha^2beta
        t0 = self[1] + self[0]
        t1 = t0.scale()
        c0 = self[0] + t1
        c1 = t1
        c0 = c0.scale2()
        c1 = c1.scale2()
        return GF2_22(c0, c1)

    def inv(self):
        t0 = self[0] + self[1]
        #square_scale = GF2_2(t0[0], t0[0] + t0[1])
        square_scale = t0.sqr().scale()
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
        t1 = t0.scale()
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
            assert fromint < 256, 'GF2_222 elemant bigger than 15.'
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
        for i in range(256 - 2):
            a = a * self
        return a

    def __getitem__(self, index):
        return self.coeff[index]

    def __repr__(self):
        return str(self.coeff)

    def __mul__(self, other):
        t0 = (self[1] + self[0]) * (other[0] + other[1])
        t1 = t0.scale()
        c1 = t1 + (self[1] * other[1])
        c0 = t1 + (self[0] * other[0])
        return GF2_22(c0, c1)

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

if __name__ == "__main__":
    main()