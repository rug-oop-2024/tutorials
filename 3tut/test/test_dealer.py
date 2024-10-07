import unittest
from unittest.mock import MagicMock, patch
from dealer import Dealer
from cards import Card

class DealerTest(unittest.TestCase):
    def setUp(self):
        """Set up a Dealer object before each test."""
        self.dealer = Dealer()

    @patch('dealer.Card')
    def test_reset(self, MockCard):
        """Test if reset method clears the hand and sets default values."""
        # Simulate the dealer having a hand
        self.dealer._cards = [MockCard(), MockCard()]
        self.dealer._score = 21
        self.dealer._first_round = False

        # Call reset
        self.dealer.reset()

        # Assert that the cards and score are reset
        self.assertEqual(self.dealer._cards, [])
        self.assertEqual(self.dealer._score, 0)
        self.assertTrue(self.dealer._first_round)

    @patch('dealer.Card')
    def test_take_card(self, MockCard):
        """Test if the dealer can take a card."""
        mock_card = MockCard()
        self.dealer.take_card(mock_card)

        # Assert that the card was added to the dealer's hand
        self.assertIn(mock_card, self.dealer._cards)

    @patch('dealer.Card')
    def test_get_score_first_round(self, MockCard):
        """Test the get_score method on the first round."""
        mock_card = MockCard()
        mock_card.rank.num_value.return_value = 10
        self.dealer._cards = [mock_card]

        self.assertTrue(self.dealer._first_round)

        # Test that the score is based on only the first card
        score = self.dealer.get_score()
        self.assertEqual(score, 10)

    @patch('dealer.Card')
    def test_get_score_after_first_round(self, MockCard):
        """Test the get_score method after the first round."""
        mock_card1 = MockCard()
        mock_card2 = MockCard()
        self.dealer._cards = [mock_card1, mock_card2]
        self.dealer._first_round = False  # Simulate moving past the first round

        # Mock the inherited get_score method
        with patch('hand.HasHand.get_score', return_value=21) as mock_get_score:
            score = self.dealer.get_score()
            mock_get_score.assert_called_once()
            self.assertEqual(score, 21)

    @patch('dealer.Card')
    def test_reveal_hand_first_round(self, MockCard):
        """Test the reveal_hand method during the first round."""
        mock_card = MockCard()
        mock_card.__str__.return_value = "Ten of Diamonds"
        mock_card.rank.num_value.return_value = 10
        self.dealer._cards = [mock_card]

        # Test that the hand is revealed with one hidden card in the first round
        hand_description = self.dealer.reveal_hand()
        expected_description = "Ten of Diamonds and one hidden card - with a score of 10"
        self.assertEqual(hand_description, expected_description)

    def test_reveal_hand_after_first_round(self):
        """Test the reveal_hand method after the first round."""
        mock_card1 = MagicMock()
        mock_card2 = MagicMock()
        mock_card1.__str__.return_value = "Ten of Diamonds"
        mock_card2.__str__.return_value = "Jack of Hearts"

        self.dealer._cards = [mock_card1, mock_card2]
        print(self.dealer._cards)
        self.dealer._first_round = False  # Simulate moving past the first round
        self.dealer._score = 21  # Mock the score

        # Test that the hand is fully revealed after the first round
        hand_description = self.dealer.reveal_hand()
        expected_description = "Ten of Diamonds, Jack of Hearts with a score of 21"
        self.assertEqual(hand_description, expected_description)


if __name__ == '__main__':
    unittest.main()
