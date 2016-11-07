"""
This module contains the :class:`Player` class.
"""


import random


class Player:
    """The Player base class.

    Args:
        coin(str): The coin representing the user.
    """

    def __init__(self, coin):

        self.coin = coin

    def play(self, board):
        """Choose a random column to play on.

        Args:
            board(:class:`Board <connect4.game.Board>`): The current board.

        Returns:
            (int): The column to play on.
        """

        found_col = 0
        while not found_col:
            col = random.randint(0, board.n_cols - 1)
            found_col = board.col_is_free(col)

        return col

    def __str__(self):

        return str(self.coin)


class Human(Player):
    """A Human player.

    Args:
        coin(str): The coin representing the user.
    """

    def __init__(self, coin):

        Player.__init__(self, coin)

    def play(self, board):
        """Ask user where he/she wants to play.

        Args:
            board(:class:`Board <connect4.game.Board>`): The current board.

        Returns:
            (int): The column to play on.
        """

        input_ok = False
        while not input_ok:
            try:
                msg = "{0}'s turn. Please choose a column:".format(self)
                col = int(input(msg)) - 1
                assert 0 <= col < board.n_cols
                assert board.col_is_free(col)
                input_ok = True
            except (ValueError, AssertionError):
                print('Invalid choice.')
                pass

        return col
