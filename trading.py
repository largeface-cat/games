# This is a card trading game for preparing for quant interviews.?)
# A standard deck of 52 cards is used, with 4 suits and 13 ranks
# A number of cards are drawn from the deck, and as the game progresses, cards are shown to the player
# We trade on an asset that is a function of the cards drawn
# Modify the function by hardcoding executable python lines into asset_str. Examples are given
# Bot trades against you according to a MC sim result.
# Try to beat it and get correct when asked to calc your PnL!
import random
from tqdm import tqdm
from copy import deepcopy
from typing import List, Callable

A_IS_1 = True
MONTE_CARLO_SIM = 10000
DEBUG = True  # Choose to cheat or not.
RED = '\033[91m'
BLACK = '\033[30m'
END = '\033[0m'
BOLD = '\033[1m'
red = [0, 1]
black = [2, 3]
asset_str = [
    "max(0, sum([card.rank for card in cards if card.suit in red])-10.5)",
    "len([card for card in cards if card.suit in red]) * sum([card.rank for card in cards if card.suit in black])",
][0]
    # the asset_str should be a line of python code that 
    # returns a float based on the `cards` variable: List[Card]


class Card():
    def __init__(self, suit:int, rank:int) -> None:
        '''
        Suit: 0-3, 0: ♥, 1: ♦, 2: ♣, 3: ♠\\
        Rank: 1-13, 1: A, 2-10: 2-10, 11: J, 12: Q, 13: K\\
        If A_IS_1 is True, A is 1, else A is 14
        '''
        self.suit = suit
        self.rank = rank
    def __str__(self):
        return f"{BOLD}{RED if self.suit in red else BLACK}|{'♥♦♣♠'[self.suit]}-{('A23456789TJQK'[self.rank - 1] if A_IS_1 else '23456789TJQKA'[self.rank - 2])}|{END}"
    def __repr__(self):
        return self.__str__()
    
class Deck():
    def __init__(self) -> None:
        self.cards = [Card(suit, rank) for suit in range(4) for rank in range(1, 14)]
    def shuffle(self):
        random.shuffle(self.cards)
    def draw(self, n):
        return [self.cards.pop() for _ in range(n)]
    def __len__(self):
        return len(self.cards)
    def __str__(self):
        return str(self.cards)
    def __repr__(self):
        return self.__str__()

class Game():
    def __init__(self) -> None:
        self.deck = Deck()
        self.deck.shuffle()
        self.n_cards = None
        self.schedule = None
        self.rounds = None
        self.current_round = 0
        self.shown_public_cards = []
        self.traded_asset = None
        self.tick_size = None
        self.max_spread_ratio = None
    def init(self, func:Callable):
        while True:
            self.n_cards = int(input('How many cards to draw: '))
            self.schedule = list(map(int, input('Schedule of drawing cards: ').split()))
            if sum(self.schedule) != self.n_cards:
                print(f'Sum of schedule {sum(self.schedule)} should be equal to number of cards to draw {self.n_cards}')
                continue
            break
        self.rounds = len(self.schedule)
        traded_asset = Asset(func)
        self.traded_asset = traded_asset
        self.tick_size = float(input('Tick size: '))
        self.max_spread_ratio = float(input('Max spread ratio (%): ')) / 100
    def draw(self):
        self.shown_public_cards += self.deck.draw(self.schedule[self.current_round])
        self.current_round += 1    

class Asset():
    def __init__(self, f:Callable) -> None:
        '''
        f: Callable, f(cards:List[Card]) -> float
        '''
        self.f = f
    def __call__(self, cards:List[Card]) -> float:
        return self.f(cards)
    def monte_carlo(self, game:Game, n_sim:int) -> float:
        result = 0
        n_to_draw = game.n_cards - len(game.shown_public_cards)
        for i in tqdm(range(n_sim)):
            branch_deck = deepcopy(game.deck)
            branch_deck.shuffle()
            cards = branch_deck.draw(n_to_draw)
            result += self.f(game.shown_public_cards + cards)
        return result / n_sim
        
class Player():
    def __init__(self, name='', cash=0, position=0) -> None:
        self.name = name
        self.cash = cash
        self.position = position
    def __str__(self):
        return f"Player {self.name}: Cash {self.cash}, Position {self.position}"
    def __repr__(self):
        return self.__str__()
    def buy(self, price, size):
        self.cash -= price * size
        self.position += size
    def sell(self, price, size):
        self.cash += price * size
        self.position -= size
    def settle(self, price):
        self.cash += price * self.position
        self.position = 0



if __name__ == '__main__':
    game = Game()
    
    print(f"Asset function: {asset_str}")
    exec(f"game.init(lambda cards: {asset_str})")
    bot = Player('Bot', 0, 0)
    player = Player('You', 0, 0)
    for rnd in range(len(game.schedule)):
        
        print(f'Round {rnd + 1}: {" ".join([str(card) for card in game.shown_public_cards])}')
        while True:
            bid = float(input('Bid: '))
            ask = float(input('Ask: '))
            mid = (bid + ask) / 2
            if bid <= 0 or (ask - bid) / bid > game.max_spread_ratio+1e-5:
                print('Spread too high, please adjust')
                continue
            elif abs(bid / game.tick_size - round(bid / game.tick_size)) > 1e-5 or abs(ask / game.tick_size - round(ask / game.tick_size)) > 1e-5:
                print(bid / game.tick_size != int(bid / game.tick_size), bid / game.tick_size, int(bid / game.tick_size))
                print(f'Price should be multiple of tick size {game.tick_size}')
                continue
            break
        size = int(input('Size: '))
        print("Bot thinking...")
        expected_value = game.traded_asset.monte_carlo(game, MONTE_CARLO_SIM)
        if DEBUG:
            print(f'Expected value: {expected_value}')
        if expected_value > mid:
            bot.buy(ask, size)
            player.sell(ask, size)
            print(f'Bot bought {size} at {ask}')
        else:
            bot.sell(bid, size)
            player.buy(bid, size)
            print(f'Bot sold {size} at {bid}')
        game.draw()
    print(f'Final: {" ".join([str(card) for card in game.shown_public_cards])}')
    true_value = game.traded_asset(game.shown_public_cards)
    print(f'True value: {true_value}')
    pnl = float(input('PnL: '))
    print(bot)
    print(player)
    bot.settle(true_value)
    player.settle(true_value)
    assert bot.cash + player.cash == 0, f"Bot cash {bot.cash}, Player cash {player.cash}"
    assert bot.position == player.position == 0, f"Bot position {bot.position}, Player position {player.position}"
    if abs(pnl - player.cash) > 1e-6:
        print(f'Wrong calculation! PnL should be {player.cash}')
    else:
        print(f'Correct calculation! PnL is {player.cash}')