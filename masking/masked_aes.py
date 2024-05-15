from __future__ import annotations

### Values are represented as a binary array
### For a = [...], a[0] is the MSB. Higher degree term on the left.
### Meanehile, a value X is represented as x^3 x^2 x^1 x^0 in the Daemen's work
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
    A list of two GF2 elements, [x1, x0].
    x1 is the MSB.
    """
    def __init__(self, elem1: GF2 = GF2(), elem0: GF2 = GF2(), fromint: int = None):
        if fromint is None:
            self.coeff = [elem1, elem0]
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
        ### Normal basis
        t = (self.coeff[0] + self.coeff[1]) * (other.coeff[0] + other.coeff[1])
        c1 = t + (self.coeff[0] * other.coeff[0])
        c0 = t + (self.coeff[1] * other.coeff[1])
        return GF2_2(c1, c0)

class GF2_4:
    """
    Name:        GF2_4
    A list of two GF2_2 elements [x1, x0], x1 and x0 are in GF2_2.
    x1 is the MSB.
    """
    def __init__(self, elem1: GF2_2 = GF2_2(), elem0: GF2_2 = GF2_2(), fromint: int = None):
        if fromint is None:
            self.coeff = [elem1, elem0]
        else:
            assert fromint < 16, 'GF2_4 elemant bigger than 15.'
            tmp = format(fromint, f'04b')
            x0 = fromint & 0x3
            x1 = fromint >> 2
            self.coeff = [GF2_2(fromint = x1), GF2_2(fromint = x0)]

    def __repr__(self):
        return str(self.coeff)

    def __mul__(self, other):
        ### Normal basis
        ### Higher (H) is 0, lower (L) is 1.
        t0 = (self.coeff[0] + self.coeff[1]) * (other.coeff[1] + other.coeff[0])
        t1 = GF2_2(t0[1], t0[0] + t0[1])
        c1 = t1 + (self.coeff[0] * other.coeff[0])
        c0 = t1 + (self.coeff[1] * other.coeff[1])
        return GF2_4(c1, c0)


def main():

    ### Test GF2_2_mul
    print("Test GF2_2_mul, (1, 1) is the unity")
    for a in range(4):
        for b in range(4):
            v_a = GF2_2(fromint = a)
            v_b = GF2_2(fromint = b)
            c = v_a * v_b
            print(f'{a, b}: {v_a} * {v_b} -> {c}')

    ### Test GF2_4_mul
    print("Test GF2_4_mul, (1, 1, 1, 1) is the unity?")
    for a in range(16):
        for b in range(16):
            v_a = GF2_4(fromint = a)
            v_b = GF2_4(fromint = b)
            c = v_a * v_b
            print(f'{a, b}: {v_a} * {v_b} -> {c}')



if __name__ == "__main__":
    main()