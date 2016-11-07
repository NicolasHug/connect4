"""
This module runs a game.
"""

from .game import Game
from .player import Human
from .player import Player


g = Game((Human('X'), Player('O')))
g.run()
