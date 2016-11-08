"""
This module runs a game.
"""

from .game import Game
from .player import Human
from .player import Player
from .player import Minimax

n_rows = 6
n_cols = 7
to_win = 4

player1 = Minimax('X', depth=4)
player2 = Minimax('O', depth=4)
player1 = Human('X')

#player1 = Player('X')
#player2 = Player('O')

g = Game((player1, player2), n_rows=n_rows, n_cols=n_cols, to_win=to_win)
g.run()
