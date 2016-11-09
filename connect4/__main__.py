"""
This module runs a game.
"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import argparse

from .game import Game
from .player import Human
from .player import Player
from .player import Minimax


def main():

    parser = argparse.ArgumentParser(
             description='Run a Connect4 game between two players',
             epilog='Example: python -m connect4 -player1 human ' +
                    '-player2 human')

    players_choices = {'human': Human,
                       'minimax': Minimax,
                       'random': Player,
                       }

    parser.add_argument('-player1', type=str,
                        default='human',
                        choices=players_choices,
                        help='The first player. ' +
                        'Allowed values are ' +
                        ', '.join(players_choices.keys()) +
                        '. (default: human)'
                        )

    parser.add_argument('-player2', type=str,
                        default='minimax',
                        choices=players_choices,
                        help='The second player. ' +
                        'Allowed values are ' +
                        ', '.join(players_choices.keys()) +
                        '. (default: minimax)'
                        )

    args = parser.parse_args()

    player1 = players_choices[args.player1]
    player2 = players_choices[args.player2]

    g = Game((player1('X'), player2('O')))
    g.run()

if __name__ == "__main__":
    main()
