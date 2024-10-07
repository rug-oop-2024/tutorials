from pydantic import PrivateAttr
from hand import HasHand
from cards import Card
from resettable import Resettable


class Dealer(HasHand, Resettable):

    def reset(self) -> None:
        self._cards = []
        self._score = 0
        self._first_round = True

    def take_card(self, card : Card) -> None:
        super().take_card(card)

    def get_score(self) -> int:
        if self._first_round:
            return self._cards[0].rank.num_value()
        return super().get_score()

    def reveal_hand(self) -> str:
        if self._first_round:
            score = self.get_score()
            self._first_round = False
            return f"{self._cards[0]} and one hidden card - with a score of {score}"
        return f"{', '.join(map(str, self._cards))} with a score of {self._score}"
