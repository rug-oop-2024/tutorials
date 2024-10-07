import unittest
from unittest.mock import MagicMock, patch
from game import Game
from cards import Deck
from player import Player
from dealer import Dealer
from options import Hit, Stand, Surrender


class GameTest(unittest.TestCase):
    def setUp(self):
        """Set up the Game object and mock dependencies before each test."""
        self.mock_deck = MagicMock()
        self.mock_player = MagicMock()
        self.mock_dealer = MagicMock()
        self.mock_hit = MagicMock()
        self.mock_stand = MagicMock()
        self.mock_surrender = MagicMock()

        # Initialize Game with mocked components
        self.game = Game(num_decks=1)
        self.game.deck = self.mock_deck
        self.game.deck._cards = [MagicMock(), MagicMock(), MagicMock()]
        self.game.player = self.mock_player
        self.game.dealer = self.mock_dealer
        self.game.options = [self.mock_hit, self.mock_stand, self.mock_surrender]

    def test_deal_cards(self):
        """Test that deal_cards correctly deals the specified number of cards to player and dealer."""
        # Deal two cards to both player and dealer
        self.game.deal_cards(2)

        # Check that player and dealer each received two cards
        self.assertEqual(self.mock_player.take_card.call_count, 2)
        self.assertEqual(self.mock_dealer.take_card.call_count, 2)

    def test_reset(self):
        """Test that reset method resets player, dealer, and the first round flag."""
        self.game.reset()

        # Verify that player and dealer reset methods were called
        self.mock_player.reset.assert_called_once()
        self.mock_dealer.reset.assert_called_once()

        # Verify that _first_round is set to True
        self.assertTrue(self.game._first_round)

    @patch('builtins.print')
    def test_check_state_player_bust(self, mock_print):
        """Test that check_state handles the case when the player busts."""
        # Simulate player score greater than 21
        self.mock_player.get_score.return_value = 22

        # Call check_state
        self.game.check_state()

        # Verify that "Player busts" is printed and a new round is triggered
        mock_print.assert_called_with("Player busts")

    @patch('builtins.print')
    def test_check_state_dealer_bust(self, mock_print):
        """Test that check_state handles the case when the dealer busts."""
        # Simulate dealer score greater than 21
        self.mock_player.get_score.return_value = 20
        self.mock_dealer.get_score.return_value = 22

        # Call check_state
        self.game.check_state()

        # Verify that "Dealer busts" is printed and a new round is triggered
        mock_print.assert_called_with("Dealer busts")

    @patch('builtins.print')
    @patch('sys.exit')  # Mock sys.exit to prevent the test from terminating
    def test_check_state_player_wins(self, mock_exit, mock_print):
        """Test that check_state handles the case when the player wins."""
        self.mock_player.get_score.return_value = 20
        self.mock_dealer.get_score.return_value = 18
        # Call check_state
        self.game.check_state()

        # Verify that "Player wins" is printed and a new round is triggered
        mock_print.assert_called_with("Player wins")
        mock_exit.assert_not_called()

    @patch('builtins.print')
    def test_check_state_tie(self, mock_print):
        """Test that check_state handles a tie."""
        self.mock_player.get_score.return_value = 20
        self.mock_dealer.get_score.return_value = 20

        # Call check_state
        self.game.check_state()

        # Verify that "It's a tie" is printed and a new round is triggered
        mock_print.assert_called_with("It's a tie")


    @patch('builtins.input')
    def test_start(self, mock_input):
        """Test the start method. Simulate a choice and check outputs."""
        self.mock_player.reveal_hand.return_value = "mocked output"
        self.mock_dealer.reveal_hand.return_value = "mocked output"

        self.mock_dealer.get_score.return_value = 18
        self.mock_player.get_score.return_value = 20
        
        # Mock the execution of the first option (Hit, Stand, Surrender)
        self.mock_hit.execute.return_value = None

        mock_input.side_effect = ['1', '2', '3']
        
        def mock_surrender_execute(_):
            self.game.end()

        self.mock_surrender.execute.side_effect = mock_surrender_execute

        with patch('builtins.print') as mock_print:
            # Simulate starting the game and choosing an option
            self.game.start()
            # Verify hands were revealed
            mock_print.assert_any_call("\nPlayer's hand: mocked output")
            mock_print.assert_any_call("Dealer's hand: mocked output\n")

        # Verify the first option (Hit) was executed
        self.mock_hit.execute.assert_called_once_with(self.game)


if __name__ == '__main__':
    unittest.main()
