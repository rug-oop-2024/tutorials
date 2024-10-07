from abc import ABC, abstractmethod
from pydantic import PrivateAttr, BaseModel


class Option(ABC, BaseModel):
    _name : str = PrivateAttr(default="")
    _description : str = PrivateAttr(default="")

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def execute(self, game) -> None:
        pass

class Hit(Option):
    _name = "Hit"
    _description = "Take another card"

    def __str__(self) -> str:
        return f"{self._name} - {self._description}"
    
    def execute(self, game) -> None:
        game.player.take_card(game.deck.draw())
        while game.dealer.get_score() < 17:
            game.dealer.take_card(game.deck.draw())

class Stand(Option):
    _name = "Stand"
    _description = "Keep current hand"

    def __str__(self) -> str:
        return f"{self._name} - {self._description}"

    def execute(self, game) -> None:
        while game.dealer.get_score() < 17:
            game.dealer.take_card(game.deck.draw())

class Surrender(Option):
    _name = "Surrender"
    _description = "Forfeit half your bet and end the round"

    def __str__(self) -> str:
        return f"{self._name} - {self._description}"
    
    def execute(self, game) -> None:
        print("You surrendered")
        game.end()
