from cards import Deck
from pydantic import BaseModel, Field, PrivateAttr
from player import Player
from dealer import Dealer
from options import Option
from resettable import Resettable


class Game(Resettable):
    deck : Deck = Field(default=None)
    player: Player = Player()
    dealer : Dealer = Dealer()
    options : list[Option] = Field([])
    _first_round : bool = PrivateAttr(default=True)
    _on : bool = PrivateAttr(default=True)

    def __init__(self, num_decks: int = 1):
        super().__init__()
        self.deck = Deck(nr_decks=num_decks)
        
        from options import Hit, Stand, Surrender
        self.options = [Hit(), Stand(), Surrender()]
    
    def deal_cards(self, nr_cards: int):
        for _ in range(nr_cards):
            self.player.take_card(self.deck.draw())
            self.dealer.take_card(self.deck.draw())

    def start(self):
        self.deal_cards(2)

        while self._on:
            print(f"\nPlayer's hand: {self.player.reveal_hand()}")
            print(f"Dealer's hand: {self.dealer.reveal_hand()}\n")
            
            if(self._first_round == False):
                self.check_state()
            self._first_round = False

            for index, option in enumerate(self.options):
                print(f"{index + 1}: {option}")
            
            try:
                choice = int(input("\nChoose an option: "))
                self.options[choice - 1].execute(self)
            except (IndexError, ValueError):
                print("Invalid choice")

    def check_state(self):
        if self.player.get_score() > 21:
            print("Player busts")
        elif self.dealer.get_score() > 21:
            print("Dealer busts")
        elif self.player.get_score() > self.dealer.get_score():
            print("Player wins")
        elif self.player.get_score() < self.dealer.get_score():
            print("Dealer wins")
        else:
            print("It's a tie")

        if len(self.deck._cards) == 0:
            print("No more cards in the deck")
            self.end()

    
    def new_round(self):
        self.reset()
        self.deal_cards(2)
        print("=========================================\n\tNEW ROUND\n=========================================")
        print(f"\nPlayer's hand: {self.player.reveal_hand()}")
        print(f"Dealer's hand: {self.dealer.reveal_hand()}\n")
    
    def reset(self):
        self.player.reset()
        self.dealer.reset()
        self._first_round = True
    
    def end(self):
        self._on = False
        print("Game over")


if __name__ == "__main__":
    game = Game()
    game.start()
