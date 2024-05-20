from aes_sbox import *
import random


def main():
    tv = 0x12
    mask = random.randint(0, 255)
    x0 = GF2_8(fromint = tv ^ mask)
    x1 = GF2_8(fromint = mask)

    x0 = AES_map.to_GF2_222(x0)
    x1 = AES_map.to_GF2_222(x1)
    print(x1)


if __name__ == "__main__":
    main()