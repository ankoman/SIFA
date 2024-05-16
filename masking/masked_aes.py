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
    A list of two GF2 elements, [x0, x1].
    x1 is the MSB. Normal basis representation.
    """
    def __init__(self, elem0: GF2 = GF2(), elem1: GF2 = GF2(), fromint: int = None):
        if fromint is None:
            self.coeff = [elem0, elem1]
        else:
            assert fromint < 4, 'GF2_2 elemant bigger than 3.'
            tmp = format(fromint, f'02b')
            self.coeff = [GF2(int(x)) for x in list(tmp)]

    def __getitem__(self, index):
        return self.coeff[index]

    def __repr__(self):
        return str(self.coeff)

    def __add__(self, other):
        return GF2_2(self.coeff[0] + other.coeff[0], self.coeff[1] + other.coeff[1])

    def __mul__(self, other):
        t = (self.coeff[1] + self.coeff[0]) * (other.coeff[1] + other.coeff[0])
        c1 = t + (self.coeff[1] * other.coeff[1])
        c0 = t + (self.coeff[0] * other.coeff[0])
        return GF2_2(c0, c1)

class GF2_22:
    """
    Name:        GF2_22
    A list of two GF2_2 elements [x0, x1], x1 and x0 are in GF2_2.
    X in GF2_2 is represented as x0*alpha + x1*alpha^2, [alpha, alpha^2] is the normal basis.
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

    def inv(self):
        print(self)
        t0 = self[0] + self[1]
        print(t0)
        square_scale = GF2_2(t0[1], t0[0] + t0[1])
        ### square scale semms bad
        print(square_scale)

        print(self[0]*self[1])
        power5 = square_scale + self[0]*self[1]
        print(power5)
        return power5
        inv = GF2_2(power5[1], power5[0])

        return GF2_22(inv * self[1], inv * self[0])

    def __getitem__(self, index):
        return self.coeff[index]

    def __repr__(self):
        return str(self.coeff)

    def __mul__(self, other):
        ### Higher (H) is 1, lower (L) is 0.
        t0 = (self.coeff[1] + self.coeff[0]) * (other.coeff[0] + other.coeff[1])
        t1 = GF2_2(t0[1], t0[1] + t0[0])
        c1 = t1 + (self.coeff[1] * other.coeff[1])
        c0 = t1 + (self.coeff[0] * other.coeff[0])
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
        print(f'{a_inv} == {a * a * a * a * a}')
        #print(f'{a} * {a_inv} -> {a * a_inv}')

if __name__ == "__main__":
    main()