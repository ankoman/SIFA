
FAULT_MODEL = "random_and_1"
N_BITS = 2
 
def hw(x: int) -> int:
    return bin(x).count("1") # python 3.9 and less

def px_i(x: int, p: float) -> float:
    ### Ineffective probability
    if FAULT_MODEL == "random_and_1":
        return p**hw(x)

dict_ineff_fault_dist = {}
dict_eff_fault_dist = {}
 
### init dist
for i in range(2**N_BITS):
    for j in range(2**N_BITS):
        dict_ineff_fault_dist[(i,j)] = 0
        dict_eff_fault_dist[(i,j)] = 0

 
for i in range(2**N_BITS):
    dict_ineff_fault_dist[(i,i)] = px_i(i, 0.5)
    dict_eff_fault_dist[(i,i)] = 1 - px_i(i, 0.5)

 
### SEI
SEI_ineff = 0
SEI_eff = 0
ineff_rate = 0
eff_rate = 0
for x in dict_ineff_fault_dist.keys():
    if x[0] == x[1]:
        SEI_ineff += (dict_ineff_fault_dist[x] - 1/4) **2
        ineff_rate += dict_ineff_fault_dist[x]
    else:

ineff_rate /= 2**N_BITS
 
print(SEI)
print(ineff_rate)
 