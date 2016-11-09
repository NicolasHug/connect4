"""
This module tests the player module.
"""

from connect4 import Player
from connect4 import Minimax
from connect4 import Game


def test_Player():

    player1 = Player('X')
    player2 = Minimax('O', depth=2)
    g = Game((player1, player2))
    g.run()
