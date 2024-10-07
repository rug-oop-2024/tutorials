import unittest
from unittest.mock import MagicMock, patch
from options import Hit, Stand, Surrender

class TestHitOption(unittest.TestCase):
    def setUp(self):
        """Set up mocks and the Hit option before each test."""
        self.hit_option = Hit()
    
    def test_str(self):
        """Test the string representation of the Hit option."""
        self.assertEqual(str(self.hit_option), "Hit - Take another card")

    def test_hit_execution_no_dealer(self):
        """Test the execution of the Hit option. No dealer."""
        game = MagicMock()
        game.dealer.get_score.return_value = 17
        game.player._cards = [MagicMock()] # simulate player having a card
        game.player.get_score.return_value = 6
        game.deck.draw.return_value = MagicMock()
        self.hit_option.execute(game)
        self.assertEqual(game.player.take_card.call_count, 1)
        self.assertEqual(game.dealer.take_card.call_count, 0)

    def test_hit_execution_yes_dealer(self):
        """Test the execution of the Hit option.Yes Dealer"""
        game = MagicMock()
        card = MagicMock()

        card.rank.num_value.return_value = 10

        game.player._cards = [MagicMock()] # simulate player having a card
        game.dealer._cards = [card] # simulate dealer having a card

        game.dealer._first_round = False
        game.player.get_score.return_value = 6 # 6
        
        game.dealer.get_score.side_effect = [10, 17] # 10, 17

        game.deck.draw.return_value = card

        self.hit_option.execute(game)
        self.assertEqual(game.player.take_card.call_count, 1)
        self.assertEqual(game.dealer.take_card.call_count, 1)

class TestStandOption(unittest.TestCase):
    def setUp(self):
        """Set up mocks and the Stand option before each test."""
        self.stand_option = Stand()

    def test_str(self):
        """Test the string representation of the Stand option."""
        self.assertEqual(str(self.stand_option), "Stand - Keep current hand")

    def test_execute(self):
        """Test that Stand executes correctly and dealer draws until score is 17 or more."""
        # Mock the game and dealer
        mock_game = MagicMock()
        mock_game.dealer = MagicMock()
        mock_game.deck = MagicMock()

        # Simulate the dealer's score increasing after each draw
        mock_game.dealer.get_score.side_effect = [16, 16, 17]

        # Execute the Stand option
        self.stand_option.execute(mock_game)

        # Verify that dealer continues to draw cards while score < 17
        self.assertEqual(mock_game.dealer.take_card.call_count, 2)


class TestSurrenderOption(unittest.TestCase):
    def setUp(self):
        """Set up mocks and the Surrender option before each test."""
        self.surrender_option = Surrender()

    def test_str(self):
        """Test the string representation of the Surrender option."""
        self.assertEqual(str(self.surrender_option), "Surrender - Forfeit half your bet and end the round")

    @patch('builtins.print')
    def test_execute(self, mock_print):
        """Test that Surrender executes correctly and ends the game."""
        # Mock the game
        mock_game = MagicMock()

        # Execute the Surrender option
        self.surrender_option.execute(mock_game)

        # Verify that the surrender message is printed
        mock_print.assert_called_once_with("You surrendered")

        # Verify that the game ends
        mock_game.end.assert_called_once()


if __name__ == '__main__':
    unittest.main()