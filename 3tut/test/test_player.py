import unittest
from unittest.mock import MagicMock
from player import Player
from cards import Card


class PlayerTest(unittest.TestCase):
    def setUp(self):
        """Set up the Player object before each test."""
        self.player = Player()

    def test_take_card(self):
        """Test that the player can take a card and the card is added to the hand."""
        mock_card = MagicMock()
        mock_card.__str__.return_value = "Ace of Spades"
        mock_card.rank.num_value.return_value = 11

        # Take a card
        self.player.take_card(mock_card)

        # Verify that the card is added to the player's hand
        self.assertIn(mock_card, self.player._cards)
        self.assertEqual(self.player._score, 11)

    def test_get_score(self):
        """Test that get_score returns the correct score."""
        mock_card1 = MagicMock()
        mock_card1.rank.num_value.return_value = 10
        mock_card2 = MagicMock()
        mock_card2.rank.num_value.return_value = 5

        # Take two cards
        self.player.take_card(mock_card1)
        self.player.take_card(mock_card2)

        # Verify that the score is correctly summed
        self.assertEqual(self.player.get_score(), 15)

    def test_reveal_hand(self):
        """Test that reveal_hand returns the correct description of the player's hand."""
        mock_card1 = MagicMock()
        mock_card1.__str__.return_value = "Ace of Spades"
        mock_card1.rank.num_value.return_value = 11
        mock_card2 = MagicMock()
        mock_card2.__str__.return_value = "King of Hearts"
        mock_card2.rank.num_value.return_value = 10

        # Take two cards
        self.player.take_card(mock_card1)
        self.player.take_card(mock_card2)

        # Verify that the hand is revealed correctly
        expected_hand_description = "Ace of Spades, King of Hearts with a score of 21"
        self.assertEqual(self.player.reveal_hand(), expected_hand_description)

    def test_reset(self):
        """Test that reset clears the player's hand and resets the score."""
        mock_card = MagicMock()
        self.player.take_card(mock_card)

        # Call reset
        self.player.reset()

        # Verify that the hand and score are reset
        self.assertEqual(self.player._cards, [])
        self.assertEqual(self.player._score, 0)


if __name__ == '__main__':
    unittest.main()
