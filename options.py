import numpy as np
import matplotlib.pyplot as plt
import random
from typing import Iterator, Callable
from copy import deepcopy
class Asset():
    def __init__(self, current_price, price_schedule:Iterator):
        self.price = current_price
        self.schedule = price_schedule
    def next(self):
        self.price *= self.schedule.__next__()

class Option():
    def __init__(self, asset:Asset, payoff:Callable, expiry:int):
        self.asset = asset
        self.payoff = payoff
        self.expiry = expiry
        self.strike = None
        self.price = None
    def calc_strike(self):
        pass
    def pricing(self, n_sim=1000, plotting=False):
        tot_ret = 0
        final_p = []
        if plotting:
            fig, ax = plt.subplots(1, 2, figsize=(10, 20))
        for i in range(n_sim):
            sim_asset = Asset(self.asset.price, self.asset.schedule)
            history = [sim_asset.price]
            for j in range(self.expiry):
                sim_asset.next()
                if plotting:
                    history.append(sim_asset.price)
            if plotting:
                ax[0].plot(history, alpha=0.1, color='r')
            tot_ret += self.payoff(sim_asset.price)
            final_p.append(sim_asset.price)
        self.price = tot_ret / n_sim
        if plotting:
            ax[1].hist(final_p, bins=100)
            fig.show()

def norm_return(alpha:float, vol:float):
    '''
    generates random normal returns
    '''
    while 1:
        yield random.normalvariate(alpha, vol) + 1

stock = Asset(2000, norm_return(0.0, 0.01))
op = Option(stock, lambda x: max(0, x-2000), 1)
op.pricing(plotting=True)
print(stock.price, op.price)
input()