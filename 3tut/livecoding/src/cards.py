import re
from pydantic import BaseModel, Field, PrivateAttr
from enum import Enum
import random

class Suit(str, Enum):
    SPADES = "♠"
    HEARTS = "♥"
    DIAMONDS = "♦"
    CLUBS = "♣"

class Rank(str, Enum):
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    TEN = "10"
    JACK = "J"
    QUEEN = "Q"
    KING = "K"
    ACE = "A"

    def num_value(self):
        if self == Rank.ACE:
            return 11
        elif self in [Rank.JACK, Rank.QUEEN, Rank.KING]:
            return 10
        else:
            return int(self)

    

class Card(BaseModel):
    suit: Suit = Field()
    rank: Rank = Field()

    def __str__(self) -> str:
        return f"{self.rank.value} of {self.suit.value}"
    

class Deck(BaseModel):
    _cards : list[Card] = PrivateAttr(default=[])


    def __init__(self, nr_decks: int = 1):
        super().__init__()

        for _ in range(nr_decks):
            [self._cards.append(Card(suit=suit, rank=rank)) for suit in Suit for rank in Rank]
        self.shuffle()

    
    def shuffle(self):
        random.shuffle(self._cards)

    def draw(self) -> Card:
        return self._cards.pop()