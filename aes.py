#!/usr/bin/env python
import pickle, sys
import numpy as np
import matplotlib.pyplot as plt

"""
    Copyright (C) 2012 Bo Zhu http://about.bozhu.me

    Permission is hereby granted, free of charge, to any person obtaining a
    copy of this software and associated documentation files (the "Software"),
    to deal in the Software without restriction, including without limitation
    the rights to use, copy, modify, merge, publish, distribute, sublicense,
    and/or sell copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
    THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
    DEALINGS IN THE SOFTWARE.
"""

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
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
)

InvSbox = (
    0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
    0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
    0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
    0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
    0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
    0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
    0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
    0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
    0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
    0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
    0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
    0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
    0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
    0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
    0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D,
)


# learnt from http://cs.ucsb.edu/~koc/cs178/projects/JT/aes.c
xtime = lambda a: (((a << 1) ^ 0x1B) & 0xFF) if (a & 0x80) else (a << 1)


Rcon = (
    0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40,
    0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A,
    0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A,
    0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39,
)

def mix_single_column(a):
    b = [0,0,0,0]
    # please see Sec 4.1.2 in The Design of Rijndael
    t = a[0] ^ a[1] ^ a[2] ^ a[3]
    u = a[0]
    b[0] = t ^ xtime(a[0] ^ a[1]) ^ a[0]
    b[1] = t ^ xtime(a[1] ^ a[2]) ^ a[1]
    b[2] = t ^ xtime(a[2] ^ a[3]) ^ a[2]
    b[3] = t ^ xtime(a[3] ^ u) ^ a[3]

    return b

def inv_mix_single_column(s):
    t = [0,0,0,0]
    # see Sec 4.1.3 in The Design of Rijndael
    u = xtime(xtime(s[0] ^ s[2]))
    v = xtime(xtime(s[1] ^ s[3]))
    t[0] = s[0] ^ u
    t[1] = s[1] ^ v
    t[2] = s[2] ^ u
    t[3] = s[3] ^ v

    return mix_single_column(t)

def sub_bytes_column(s):
    t = []
    for i in range(4):
        t.append(Sbox[s[i]])
    return t

def inv_sub_bytes_column(s):
    t = []
    for i in range(4):
        t.append(InvSbox[s[i]])
    return t

def text2matrix(text):
    matrix = []
    for i in range(16):
        byte = (text >> (8 * (15 - i))) & 0xFF
        if i % 4 == 0:
            matrix.append([byte])
        else:
            matrix[i // 4].append(byte)
    return matrix


def matrix2text(matrix):
    text = 0
    for i in range(4):
        for j in range(4):
            text |= (matrix[i][j] << (120 - 8 * (4 * i + j)))
    return text

def text2column(text):
    column = []
    for i in range(4):
        byte = (text >> (8 * (3 - i))) & 0xFF
        column.append(byte)
    return column

def column2text(column):
    text = 0
    for i in range(4):
        text |= (column[i] << (24 - 8 * i))
    return text

class AES:
    def __init__(self, master_key):
        self.change_key(master_key)

    def change_key(self, master_key):
        self.round_keys = text2matrix(master_key)
        # print self.round_keys

        for i in range(4, 4 * 11):
            self.round_keys.append([])
            if i % 4 == 0:
                byte = self.round_keys[i - 4][0]        \
                     ^ Sbox[self.round_keys[i - 1][1]]  \
                     ^ Rcon[i // 4]
                self.round_keys[i].append(byte)

                for j in range(1, 4):
                    byte = self.round_keys[i - 4][j]    \
                         ^ Sbox[self.round_keys[i - 1][(j + 1) % 4]]
                    self.round_keys[i].append(byte)
            else:
                for j in range(4):
                    byte = self.round_keys[i - 4][j]    \
                         ^ self.round_keys[i - 1][j]
                    self.round_keys[i].append(byte)

        # print self.round_keys

    def encrypt(self, plaintext):
        self.plain_state = text2matrix(plaintext)

        self.__add_round_key(self.plain_state, self.round_keys[:4])

        for i in range(1, 10):
            self.__round_encrypt(self.plain_state, self.round_keys[4 * i : 4 * (i + 1)])

        self.__sub_bytes(self.plain_state)
        self.__shift_rows(self.plain_state)
        self.__add_round_key(self.plain_state, self.round_keys[40:])

        return matrix2text(self.plain_state)

    def decrypt(self, ciphertext):
        self.cipher_state = text2matrix(ciphertext)

        self.__add_round_key(self.cipher_state, self.round_keys[40:])
        self.__inv_shift_rows(self.cipher_state)
        self.__inv_sub_bytes(self.cipher_state)

        for i in range(9, 0, -1):
            self.__round_decrypt(self.cipher_state, self.round_keys[4 * i : 4 * (i + 1)])

        self.__add_round_key(self.cipher_state, self.round_keys[:4])

        return matrix2text(self.cipher_state)

    def __add_round_key(self, s, k):
        for i in range(4):
            for j in range(4):
                s[i][j] ^= k[i][j]


    def __round_encrypt(self, state_matrix, key_matrix):
        self.__sub_bytes(state_matrix)
        self.__shift_rows(state_matrix)
        self.__mix_columns(state_matrix)
        self.__add_round_key(state_matrix, key_matrix)


    def __round_decrypt(self, state_matrix, key_matrix):
        self.__add_round_key(state_matrix, key_matrix)
        self.__inv_mix_columns(state_matrix)
        self.__inv_shift_rows(state_matrix)
        self.__inv_sub_bytes(state_matrix)

    def __sub_bytes(self, s):
        for i in range(4):
            for j in range(4):
                s[i][j] = Sbox[s[i][j]]


    def __inv_sub_bytes(self, s):
        for i in range(4):
            for j in range(4):
                s[i][j] = InvSbox[s[i][j]]


    def __shift_rows(self, s):
        s[0][1], s[1][1], s[2][1], s[3][1] = s[1][1], s[2][1], s[3][1], s[0][1]
        s[0][2], s[1][2], s[2][2], s[3][2] = s[2][2], s[3][2], s[0][2], s[1][2]
        s[0][3], s[1][3], s[2][3], s[3][3] = s[3][3], s[0][3], s[1][3], s[2][3]


    def __inv_shift_rows(self, s):
        s[0][1], s[1][1], s[2][1], s[3][1] = s[3][1], s[0][1], s[1][1], s[2][1]
        s[0][2], s[1][2], s[2][2], s[3][2] = s[2][2], s[3][2], s[0][2], s[1][2]
        s[0][3], s[1][3], s[2][3], s[3][3] = s[1][3], s[2][3], s[3][3], s[0][3]

    def __mix_single_column(self, a):
        # please see Sec 4.1.2 in The Design of Rijndael
        t = a[0] ^ a[1] ^ a[2] ^ a[3]
        u = a[0]
        a[0] ^= t ^ xtime(a[0] ^ a[1])
        a[1] ^= t ^ xtime(a[1] ^ a[2])
        a[2] ^= t ^ xtime(a[2] ^ a[3])
        a[3] ^= t ^ xtime(a[3] ^ u)


    def __mix_columns(self, s):
        for i in range(4):
            self.__mix_single_column(s[i])


    def __inv_mix_columns(self, s):
        # see Sec 4.1.3 in The Design of Rijndael
        for i in range(4):
            u = xtime(xtime(s[i][0] ^ s[i][2]))
            v = xtime(xtime(s[i][1] ^ s[i][3]))
            s[i][0] ^= u
            s[i][1] ^= v
            s[i][2] ^= u
            s[i][3] ^= v

        self.__mix_columns(s)


def xt(a):
    a = a << 1
    if a > 255:
        a -= 256
        a ^= 0x1b
    return a

def ptxt2text(ptxt):
    tmp = 0
    for elem in ptxt:
        tmp <<= 16
        tmp += elem
    return tmp

def ctxt2text(ctxt):
    tmp = 0
    for elem in ctxt:
        tmp <<= 8
        tmp += int(elem)
    return tmp

def pkl():
    f_path = r'/mnt/c/Users/sakamoto/Desktop/data_0626/random1_30000.pkl'
    ptxts = []
    with open(f_path, 'rb') as f:
        ptxts = pickle.load(f)[:2999]

    f_path = r'/mnt/c/Users/sakamoto/Desktop/data_0626/ciphertext_random1_N=3000_Period=60_Round=9_Delay=10_220905_pprm1_50ns_10bit.pkl'
    ctxts_fault = []
    with open(f_path, 'rb') as f:
        ctxts_fault = pickle.load(f)

    master_key = 0x2b7e151628aed2a6abf7158809cf4f3c
    aes = AES(master_key)
    round_key = [aes.round_keys[4 * i : 4 * (i + 1)] for i in range(10)]
    target_key = matrix2text(round_key[9])
    print(f"Traget key: {target_key:x}")

    list_ptxt = []
    list_ctxt = []
    for ptxt in ptxts:
        ptxt = ptxt2text(ptxt)
        ctxt = aes.encrypt(ptxt)
        list_ptxt.append(ptxt)
        list_ctxt.append(ctxt)
    
    with open('./ptxt.pkl', 'wb') as f:
        pickle.dump(list_ptxt, f)

    with open('./ctxt.pkl', 'wb') as f:
        pickle.dump(list_ctxt, f)

def inv_last_round(aes, ctxt):
    aes.cipher_state = text2matrix(ctxt)

    aes._AES__add_round_key(aes.cipher_state, aes.round_keys[40:])
    #aes._AES__inv_shift_rows(aes.cipher_state)
    aes._AES__inv_sub_bytes(aes.cipher_state)

    return aes.cipher_state

def make_list(aes, ctxts, ctxts_fault, target_byte):

    list_00 = [0] * 8
    list_01 = [0] * 8
    list_10 = [0] * 8
    list_11 = [0] * 8

    row = target_byte % 4
    column = target_byte // 4

    for ctxt, ctxt_f in zip(ctxts, ctxts_fault):
        y0 = inv_last_round(aes, ctxt)[column][row]
        y1 = inv_last_round(aes, ctxt2text(ctxt_f))[column][row]

        for i in range(8):
            b0 = (y0 >> i) & 1
            b1 = (y1 >> i) & 1
            if b0 == 0:
                if b1 == 0:
                    list_00[i] += 1
                else:
                    list_01[i] += 1
            else:
                if b1 == 0:
                    list_10[i] += 1
                else:
                    list_11[i] += 1

    return list_00, list_01, list_10, list_11

    
def main(N_TRACES = 1000):
    
    f_path = r'./ctxt.pkl'
    ctxts = []
    with open(f_path, 'rb') as f:
        ctxts = pickle.load(f)[:N_TRACES]

    f_path = r'/mnt/c/Users/sakamoto/Desktop/data_0626/ciphertext_random1_N=3000_Period=50_Round=9_Delay=10_220905_pprm1_50ns_10bit.pkl'
    # f_path = r'/mnt/c/Users/sakamoto/Desktop/glitcher_0625/ctlst_glitch_width=4.6ns'
    ctxts_fault = []
    with open(f_path, 'rb') as f:
        ctxts_fault = pickle.load(f)[:N_TRACES]

    master_key = 0x2b7e151628aed2a6abf7158809cf4f3c
    aes = AES(master_key)

    fig, ax = plt.subplots(figsize=(16, 8), nrows=4, ncols=4, sharex=False)
    for target_byte in range(16):
        list_00, list_01, list_10, list_11 = make_list(aes, ctxts, ctxts_fault, target_byte)

        print(' ', end='')
        for i in range(7, -1, -1):
            print(f'{i} ', end='')
        print()
        print('0->0 ', end='')
        for i in range(7, -1, -1):
            print(f'{list_00[i]} ', end='')
        print()
        print('1->1 ', end='')
        for i in range(7, -1, -1):
            print(f'{list_11[i]} ', end='')
        print()
        print('0->1 ', end='')
        for i in range(7, -1, -1):
            print(f'{list_01[i]} ', end='')
        print()
        print('1->0 ', end='')
        for i in range(7, -1, -1):
            print(f'{list_10[i]} ', end='')
        print()

        col = target_byte // 4
        row = target_byte % 4
        ax[row, col].bar([0,1,2,3,4,5,6,7], list_10)
        ax[row, col].bar([0,1,2,3,4,5,6,7], list_01, bottom = list_10)
        ax[row, col].invert_xaxis()
    plt.show()

if __name__ == '__main__':

    N_TRACES = 1000
    if len(sys.argv) > 1:
        N_TRACES = int(sys.argv[1])
    main(N_TRACES)