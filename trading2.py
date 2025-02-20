# This is a card trading game for preparing for quant interviews
# A standard deck of 52 cards is used, with 4 suits and 13 ranks
# A number of cards are drawn from the deck, and as the game progresses, cards are shown to the player
# We trade on an asset that is a function of the cards drawn
import random
from tqdm import tqdm
from copy import deepcopy
from typing import List, Callable

A_IS_1 = True
MONTE_CARLO_SIM = 10000
DEBUG = True
RED = '\033[91m'
BLACK = '\033[30m'
END = '\033[0m'
BOLD = '\033[1m'
red = [0, 1]
black = [2, 3]
asset_str = [
    "sum([card.rank for card in cards if card.suit in red])",
    "max(0, sum([card.rank for card in cards if card.suit in red])-10.5)",
    "len([card for card in cards if card.suit in red]) * sum([card.rank for card in cards if card.suit in black])",
][0]
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
    def init(self, func:Callable, n:int):
        self.n_cards = n
        traded_asset = Asset(func)
        self.traded_asset = traded_asset
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

if __name__ == '__main__':
    game = Game()
    exec(f"game.init(lambda cards: {asset_str}, int(input('num of total cards:')))")
    while True:
        # game.shown_public_cards = list(map(lambda x: Card(int(x[0]), int(x[2:])), input().split()))
        text_card = input("input current card:").split()
        game.shown_public_cards.append(Card(text_card[0], text_card[1]))
        expected_value = game.traded_asset.monte_carlo(game, MONTE_CARLO_SIM)
        print(expected_value)
       