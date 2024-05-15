import random

def toffoli(a: bool, b: bool, c: bool):
    return a ^ (b & c), b, c

def masked_toffoli(a0: bool, a1: bool, b0: bool, b1: bool, c0: bool, c1: bool):
    a0, b0, c1 = toffoli(a0, b0, c1)
    a0, b0, c0 = toffoli(a0, b0, c0)
    a1, b1, c1 = toffoli(a1, b1, c1)
    a1, b1, c0 = toffoli(a1, b1, c0)
    return a0, a1, b0, b1, c0, c1


def main():
    ### Toffoli test
    for i in range(8):
        c = i & 1
        b = (i >> 1) & 1
        a = (i >> 2) & 1
        print(f'{a, b, c} -> {toffoli(a, b, c)}')

    print()

    ### Masked toffoli test
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


if __name__ == "__main__":
    main()