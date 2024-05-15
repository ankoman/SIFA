

### Values are represented as a binary array
### For a = [...], a[0] is the MSB
### Meanehile, a value X is represented as x^3 x^2 x^1 x^0 in the Daemen's work
def GF2_2_mul(a: list, b: list) -> list:
    t = (a[0] ^ a[1]) & (b[0] ^ b[1])
    c0 = t ^ (a[0] & b[0])
    c1 = t ^ (a[1] & b[1])
    return [c0, c1]
    
def int2barray(val: int, zpad: int) -> list:
    tmp = format(val, f'0{zpad}b')
    return [int(x) for x in list(tmp)]

def main():

    ### Test GF2_2_mul
    for a in range(4):
        for b in range(4):
            v_a = int2barray(a, 2)
            v_b = int2barray(b, 2)
            c = GF2_2_mul(v_a, v_b)
            print(f'{a, b}: {v_a} * {v_b} -> {c}')



if __name__ == "__main__":
    main()