from pydantic import BaseModel
from hand import HasHand
from resettable import Resettable


class Player(HasHand, Resettable):
    def take_card(self, card) -> None:
        super().take_card(card)

    def get_score(self) -> int:
        return super().get_score()

    def reveal_hand(self) -> str:
        return f"{', '.join(map(str, self._cards))} with a score of {self._score}"
    
    def reset(self):
        self._cards = []
        self._score = 0
        return self