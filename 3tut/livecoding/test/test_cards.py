import unittest

class TestCards(unittest.TestCase):
    def test_suite(self):
        from cards import Suit
        self.assertEqual(Suit.SPADES.value, "♠")
        self.assertEqual(Suit.HEARTS.value, "♥")
        self.assertEqual(Suit.DIAMONDS.value, "♦")
        self.assertEqual(Suit.CLUBS.value, "♣")
    
    def test_rank(self):
        from cards import Rank
        self.assertEqual(Rank.TWO.num_value(), 2)
        self.assertEqual(Rank.THREE.num_value(), 3)
        self.assertEqual(Rank.FOUR.num_value(), 4)
        self.assertEqual(Rank.FIVE.num_value(), 5)
        self.assertEqual(Rank.SIX.num_value(), 6)
        self.assertEqual(Rank.SEVEN.num_value(), 7)
        self.assertEqual(Rank.EIGHT.num_value(), 8)
        self.assertEqual(Rank.NINE.num_value(), 9)
        self.assertEqual(Rank.TEN.num_value(), 10)
        self.assertEqual(Rank.JACK.num_value(), 10)
        self.assertEqual(Rank.QUEEN.num_value(), 10)
        self.assertEqual(Rank.KING.num_value(), 10)
        self.assertEqual(Rank.ACE.num_value(), 11)

    def test_card(self):
        from cards import Card, Suit, Rank
        for suit in Suit:
            for rank in Rank:
                card = Card(suit=suit, rank=rank)
                self.assertEqual(str(card), f"{rank.value} of {suit.value}")
    
    def test_deck(self):
        from cards import Deck
        deck = Deck(nr_decks=1)
        self.assertEqual(len(deck._cards), 52)
        deck.shuffle()
        self.assertEqual(len(deck._cards), 52)
        card = deck.draw()

    def test_deck_multiple_decks(self):
        from cards import Deck
        deck = Deck(nr_decks=2)
        self.assertEqual(len(deck._cards), 104)
        deck.shuffle()
        self.assertEqual(len(deck._cards), 104)
        card = deck.draw()
        self.assertEqual(len(deck._cards), 103)

if __name__ == '__main__':
    unittest.main()
