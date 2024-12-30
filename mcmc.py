import sorobn as hh
import pandas as pd
import random

bn = hh.BayesNet(
    ('C', ['S', 'R']),
    ('S', 'W'),
    ('R', 'W'))
bn.P['C'] = pd.Series({True: 0.5, False:0.5})
bn.P['S'] = pd.Series({
    (True, True): 0.1, (True, False): 0.9,
    (False, True): 0.5, (False, False): 0.5})
bn.P['R'] = pd.Series({
    (True, True): 0.8, (True, False): 0.2,
    (False, True): 0.2, (False, False): 0.8})
bn.P['W'] = pd.Series({
    (True, True, True): 0.99, (True, True, False): 0.01,
    (True, False, True): 0.9, (True, False, False): 0.1,
    (False, True, True): 0.95, (False, True, False): 0.05,
    (False, False, True): 0.05, (False, False, False): 0.95})
bn.prepare()
bn.query('C', event={'S': False, 'W': True}).values[1]


print("Part A. The sampling probabilities")
print(f"P(C|-s,r) = <{bn.query('C', event={'S': False, 'R': True}).values[1]:.4f}, {bn.query('C', event={'S': False, 'R': True}).values[0]:.4f}>")
print(f"P(C|-s,-r) = <{bn.query('C', event={'S': False, 'R': False}).values[1]:.4f}, {bn.query('C', event={'S': False, 'R': False}).values[0]:.4f}>")
print(f"P(R|c,-s,w) = <{bn.query('R', event={'C': True, 'S': False, 'W': True}).values[1]:.4f}, {bn.query('R', event={'C': True, 'S': False, 'W': True}).values[0]:.4f}>")
print(f"P(R|-c,-s,w) = <{bn.query('R', event={'C': False, 'S': False, 'W': True}).values[1]:.4f}, {bn.query('R', event={'C': False, 'S': False, 'W': True}).values[0]:.4f}>\n")


print("Part B. The transition probability matrix")
Q = [[0 for i in range(4)] for j in range(4)]
t = [(1,1), (1,0), (0,1), (0,0)]
for i in range(4):
    for j in range(4):
        if i == j:
            Q[i][j] = 0.5*bn.query('C', event={'S': False, 'R': t[j][1]}).values[t[j][0]] + 0.5*bn.query('R', event={'C': t[j][0], 'S': False, 'W': True}).values[t[j][1]]
        elif i + j == 3:
            Q[i][j] = 0
        elif i + j == 2 or i + j == 4:
            Q[i][j] = 0.5*bn.query('C', event={'S': False, 'R': t[j][1]}).values[t[j][0]]
        elif i + j == 1 or i + j == 5:
            Q[i][j] = 0.5*bn.query('R', event={'C': t[j][0], 'S': False, 'W': True}).values[t[j][1]]

print("    S1       S2       S3       S4")
for i in range(4):
    print(f"S{i+1}   ", end='')
    for j in range(4):
        print(f"{Q[j][i]:.4f}   ", end='')
    print()
print()


print("Part C. The probability for the query P(C|-s,w)")
print(f"Exact probability: <{bn.query('C', event={'S': False, 'W': True}).values[1]:.4f}, {bn.query('C', event={'S': False, 'W': True}).values[0]:.4f}>")
for i in range(3, 7):
    n = 10**i
    count_f = 0
    count_t = 0
    for _ in range(n):
        c = random.random()
        s = random.random()
        r = random.random()
        w = random.random()

        if c < 0.5:  # C = True
            if s <= 0.9 and r <= 0.8:  # S = False, R = True
                if w < 0.95:  # W = True
                    count_t += 1
            elif s <= 0.9 and r > 0.8:  # S = False, R = False
                if w < 0.05:  # W = True
                    count_t += 1
        else:  # C = False
            if s < 0.5:
                if s <= 0.5 and r <= 0.2:  # S = False, R = True
                    if w < 0.95:  # W = True
                        count_f += 1
                elif s <= 0.5 and r > 0.2:  # S = False, R = False
                    if w < 0.05:  # W = True
                        count_f += 1
    error = abs((bn.query('C', event={'S': False, 'W': True}).values[1] - count_t / (count_t + count_f)) /
                 bn.query('C', event={'S': False, 'W': True}).values[1])
    print(f"n = 10 ^ {i}: <{count_t/(count_t + count_f):.4f}, {count_f/(count_t + count_f):.4f}>, error = {100*error:.2f}%")

