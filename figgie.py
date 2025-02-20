# %%
import math
import traceback
# import numpy as np
# import matplotlib as plt
class bcolors:
    PINK = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOw = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# %%
def C(n, m):
    return math.factorial(n) // math.factorial(m) // math.factorial(n-m)
C(4,2)

# %%
# Spade, Club, Diamond, Heart
suite = ['S     ', 'C     ', 'D     ', 'H     ']
comb = [[12,10,10,8],[12,10,8,10],[12,8,10,10],
        [10,12,10,8],[10,12,8,10],[8,12,10,10],
        [10,10,12,8],[10,8,12,10],[8,10,12,10],
        [10,10,8,12],[10,8,10,12],[8,10,10,12]]
val_ind = [1, 1, 1, 0, 0, 0, 3, 3, 3, 2, 2, 2, ]

def ll(res, obs):
    return DRAW_PROB * C(res[0], obs[0]) * C(res[1], obs[1]) * C(res[2], obs[2]) * C(res[3], obs[3])

def calc(obs):
    ret = {}
    for i in range(len(comb)):
        res = comb[i]
        likelihood = ll(res, obs)
        evid = PRIOR * sum(ll(r, obs) for r in comb)
        name = ''
        for j in range(len(res)):
            if j == val_ind[i]:
                name += f'{bcolors.YELLOw}'+(f'{res[j]},   ' if res[j]>8 else '8,    ')+f'{bcolors.ENDC}'
            else:
                name += f'{res[j]},   ' if res[j]>8 else '8,    '
        ret[name] = (round(likelihood * PRIOR / evid, 5), val_ind[i])
    return dict(sorted(sorted(ret.items(), key=lambda x:x[0], reverse=True), key=lambda x:x[1], reverse=True))

# %%
if __name__ == '__main__':
    N_PLAYERS = int(input("Num of players:"))
    PRIOR = 1/12
    DRAW_PROB = 1/C(40,40//N_PLAYERS)
    while 1:
        try:
            obs = list(map(int, input(f"{bcolors.PINK}Spade Club Diamond Heart:{bcolors.ENDC}\n").split()))
            try:
                assert len(obs) == 4, "Must be a suite"
                assert sum(obs) == 40//N_PLAYERS, f"Must have a sum of {40//N_PLAYERS}"
                assert sum(i>=0 for i in obs) == 4, f"Must be non-negative"
            except AssertionError:
                traceback.print_exc()
                continue
            for i in suite: print(f'{bcolors.BLUE}{i}{bcolors.ENDC}', end='')
            print()
            probs = calc(obs)
            for i in probs.keys():
                print(f"{i}: {probs[i][0]*100:.2f}%")
            prob_sums = [0] * 4
            for i in probs.keys():
                prob_sums[probs[i][1]] += probs[i][0]
            for i in prob_sums:
                if i == max(prob_sums):
                    print(f'{bcolors.RED}{bcolors.BOLD}{i*100:.1f}% {bcolors.ENDC}', end='')
                else:
                    print(f'{i*100:.1f}% ', end='')
            print('\n-----------------------')
        except KeyboardInterrupt:
            N_PLAYERS = int(input("Num of players:"))
            PRIOR = 1/12
            DRAW_PROB = 1/C(40,40//N_PLAYERS)
            continue