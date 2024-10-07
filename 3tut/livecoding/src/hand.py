from abc import ABC, abstractmethod
from pydantic import BaseModel, PrivateAttr
from typing import List

from cards import Card

class HasHand(BaseModel, ABC):
    _cards: List[Card] = PrivateAttr(default=[])
    _score: int = PrivateAttr(default=0)

    @abstractmethod
    def take_card(self, card: Card) -> None:
        self._cards.append(card)
        self._score += card.rank.num_value()

    @abstractmethod
    def reveal_hand(self) -> str:
        pass

    @abstractmethod
    def get_score(self) -> int:
        return self._score

    @property
    def score(self):
        return self._score