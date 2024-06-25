import scipy, math

def hw(x: int) -> int:
    return bin(x).count("1") # python 3.9 and less

for PROB in [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]:
    for N_BITS in range(1, 9, 1):

        power_N = 2**N_BITS
        k = power_N - 1
        probit = scipy.stats.norm.ppf(1-2**-8)
        sd_W_max = math.sqrt(2*k)

        #print(f"\nN_BITS = {N_BITS}")
        sum = 0
        for i in range(power_N):
            sum += PROB**hw(i)

        capa = 0
        for i in range(2**N_BITS):
            capa += ((PROB**hw(i)/sum) - 1/power_N)**2
        capa *= power_N
        N_CHI = sd_W_max*probit/capa


        #print(capa, end=',')
        print(N_CHI, end=',')
    print()

