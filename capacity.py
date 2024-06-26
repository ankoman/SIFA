import scipy, math

def hw(x: int) -> int:
    return bin(x).count("1") # python 3.9 and less

for PROB in [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]:
    for N_BITS in range(1, 9, 1):

        power_N = 2**N_BITS
        k = 2**3
        probit = scipy.stats.norm.ppf(1-2**-8)
        sd_W_max = math.sqrt(2*k)

        #print(f"\nN_BITS = {N_BITS}")
        sum = 0
        for i in range(power_N):
            sum += PROB**hw(i)

        capa = 0
        for i in range(power_N):
            capa += ((PROB**hw(i)/sum) - 1/power_N)**2
        capa *= power_N
        N_CHI = sd_W_max*probit/capa


        #print(capa, end=',')
        print(N_CHI, end=',')
    print()

# ### 8bitsのうちのNbitsにしかフォールトはいらず、8bitsモデルで解析した場合 -> 結局上と一緒
# for PROB in [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]:
#     for N_BITS in range(1, 9, 1):

#         eight = 8
#         power_8 = 2**eight
#         power_N = 2**N_BITS
#         k = power_N - 1
#         probit = scipy.stats.norm.ppf(1-2**-eight)
#         sd_W_max = math.sqrt(2*k)

#         #print(f"\nN_BITS = {N_BITS}")
#         sum = 0
#         for i in range(power_N):
#             sum += PROB**hw(i)
#         sum *= 2**(eight - N_BITS)

#         capa = 0
#         for i in range(power_N):
#             capa += ((PROB**hw(i)/sum) - 1/power_8)**2
#         capa *= 2**(eight - N_BITS)
#         capa *= power_8
#         N_CHI = sd_W_max*probit/capa


#         print(capa, end=',')
#         #print(N_CHI, end=',')
#     print()

