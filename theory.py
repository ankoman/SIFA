import collections

def HW(x):
    return bin(x).count("1")

def lsb_reset(x):
    return x & 0xfe # LSB reset

n_b = 256
n_l = 9
leak_f = HW
fault_f = lsb_reset
adv = 2.6600674
s_w = 22.58317958127242
mu_w_ = 315

dist_bin = [1/256, 8/256, 28/256, 56/256, 70/256, 56/256, 28/256, 8/256, 1/256]

def make_fault_prob():
    list_fault = []
    for x in range(n_b):
        xp = lsb_reset(x)
        l = leak_f(xp)
        list_fault.append(l)
    print(list_fault)

    list_p = []
    for i in range(n_l):
        list_p.append(list_fault.count(i) / n_b)
    print(list_p)

    return list_p

def calc_capacity(list_p, list_t):
    cap = 0
    for x in range(n_b):
        xp = lsb_reset(x)
        if x == xp:
            l = leak_f(x)
            cap += (list_p[l] - list_t[l])**2 / list_t[l]

    return cap

### 1 bit set/reset fault model
### HW leak model
### CHI2 statistics
k = n_b - 1

list_p = make_fault_prob()
cap = calc_capacity(list_p, dist_bin)
print(cap)

### 1 bit set/reset fault model
### 8bits leak model
### CHI2 statistics

