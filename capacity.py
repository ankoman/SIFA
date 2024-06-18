
FAULT_MODEL = "random_and_1"
PROB = 0.9
N_BITS = 8
 
def hw(x: int) -> int:
    return bin(x).count("1") # python 3.9 and less

def sx(x: int) -> float:
    return 1/2**N_BITS

def px_i(x: int, p: float) -> float:
    ### Ineffective probability
    if FAULT_MODEL == "random_and_1":
        return p**hw(x)

### SEI
ineff_SEI = 0
eff_SEI = 0
ineff_rate = 0
eff_rate = 0

for j in range(2**N_BITS):
    ineff_SEI += (px_i(j, PROB) - sx(j)) **2
    ineff_rate += px_i(j, PROB)
    eff_SEI += ((1 - px_i(j, PROB)) - sx(j)) **2
    eff_rate += 1 - px_i(j, PROB)

ineff_capacity = 0
eff_capacity = 0
for j in range(2**N_BITS):
    ineff_capacity += (px_i(j, PROB) / ineff_rate - sx(j)) **2
    eff_capacity += ((1 - px_i(j, PROB)) / eff_rate - sx(j)) **2

ineff_capacity *= 2**N_BITS
eff_capacity *= 2**N_BITS
ineff_rate /= 2**N_BITS
eff_rate /= 2**N_BITS

print("Ineffective ")
print(f"SEI: {ineff_SEI}, rate: {ineff_rate}, capacity: {ineff_capacity}, N: {1/ineff_rate/ineff_capacity}")
print("Effective ")
print(f"SEI: {eff_SEI}, rate: {eff_rate}, capacity: {eff_capacity},  N: {1/eff_rate/eff_capacity}")