"""
This module contains the :class:`Board` and the :class:`Game` class.
"""

# Note: some (great) implementation ideas were inspired by Patrick Westerhoff:
# https://gist.github.com/poke/6934842

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from itertools import chain
from itertools import groupby

try:
    input = raw_input
except NameError:
    pass


class Board:
    """The Board class.

    Args:
        n_rows(int): The number of rows of the board.
        n_cols(int): The number of columns of the board.

    Attributes:
        n_rows(int): The number of rows of the board.
        n_cols(int): The number of columns of the board.
        grid(list of list): The proper board, represented as a ``n_rows`` *
            ``n_cols`` matrix.
    """

    EMPTY = '.'

    def __init__(self, n_rows, n_cols):

        self.n_rows = n_rows
        self.n_cols = n_cols
        self.grid = [[self.EMPTY] * n_cols for _ in range(n_rows)]

    def insert(self, col, coin):
        """Insert a piece in given column.

        Args:
            col(int): The column.
            coin(str): The coin to insert.

        Returns:
            row(int): The row where the coin was inserted.
        Raises:
            ValueError: if ``col`` is full or is out of range.
        """

        if col < 0 or col >= self.n_cols:
            raise ValueError('Invalid column ' + str(col) + '.')

        try:
            r = next(r for r in range(self.n_rows - 1, -1, -1)
                     if self.grid[r][col] == self.EMPTY)
            self.grid[r][col] = coin
        except StopIteration:
            raise ValueError('Column ' + str(col) + ' is already full.')

        return r

    def is_free(self, col):
        """Check if a coin can be inserted in given column.

        Args:
            col(int): The column

        Returns:
            ``True`` if the column is free, else ``False``.
        """

        return self.grid[0][col] == self.EMPTY

    def free_columns(self):
        """Generator function to iterate over all free columns

        Returns:
            All free columns."""

        return (col for col in range(self.n_cols) if self.is_free(col))

    def is_full(self):
        """Check if the board is full.

        Returns:
            ``True`` if the board is full, else ``False``.
        """

        return all(not self.is_free(col) for col in range(self.n_cols))

    def all_sequences(self, to_win=1):
        """Generator function to iterate over all sequences of the board.

        A sequence is either a row, a column or a diagonal.

        Args:
            to_win(int, optional): The number of successive coins needed to win
                a game. Only diagonals with a length greater or equal to
                ``to_win`` will be yielded.

        Returns:
            All sequences.
        """

        def diagonals():
            """Generator function to iterate over all the diagonals."""

            # Note : we actually yield a list and not just a generator so that
            # diagonals can be iterated multiple times.

            start = to_win - 1
            end = self.n_rows + self.n_cols - to_win
            pos_diag_indices = (((r - c, c) for c in range(self.n_cols))
                                for r in range(start, end))
            start = to_win - self.n_cols
            end = self.n_rows - to_win + 1
            neg_diag_indices = (((r + c, c) for c in range(self.n_cols))
                                for r in range(start, end))

            for d in chain(pos_diag_indices, neg_diag_indices):
                yield [self.grid[i][j] for (i, j) in d
                       if 0 <= i < self.n_rows and
                       0 <= j < self.n_cols]

        rows = self.grid
        columns = zip(*self.grid)

        return chain(rows, columns, diagonals())

    def __str__(self):

        s = ' '.join('{0:2s}'.format(str(i + 1))
                     for i in range(self.n_cols)) + '\n'
        s += '\n'.join('  '.join(cell for cell in row)
                       for row in self.grid)
        return s


class Game:
    """A basic engine for the connect4 game.

    Args:
        players(tuple of :class:`Player <connect4.player.Player>`): The two
            players. The first one is first to play.
        n_rows(int): The number of rows of the board. Default is ``6``.
        n_cols(int): The number of columns of the board. Default is ``7``.
        to_win(int): The number of aligned pieces required to win the game.
            Default is ``4``.

    Attributes:
        player1(:class:`Player <connect4.player.Player>`): The first
            player.
        player2(:class:`Player <connect4.player.Player>`): The second
            player.
        board(:class:`Board`): The board.
        to_win(int): The number of aligned pieces required to win the game.
        """

    def __init__(self, players, n_rows=6, n_cols=7, to_win=4):

        self.board = Board(n_rows, n_cols)

        self.player1, self.player2 = players
        self.player1.opponent = self.player2
        self.player2.opponent = self.player1

        self.to_win = self.player1.to_win = self.player2.to_win = to_win

        if self.player1.coin == self.player2.coin:
            raise ValueError('Both players have the same coin.')

    def check_winner(self):
        """Check if there's a winner at the current game state.

        Returns:
            :class:`Player <connect4.player.Player>`: The winner.  If no
            player has won yet, ``None`` is returned.
        """

        # for every line, column and diag, check if there are at least 'to_win'
        # pieces of the same color that are aligned.
        for sequence in self.board.all_sequences():
            for coin, group in groupby(sequence):
                if (coin != self.board.EMPTY and
                   len(list(group)) >= self.to_win):
                    return (self.player1 if coin == self.player1.coin else
                            self.player2)

        return None

    def run(self):
        """Run a game session between the two players.

        Returns:
            :class:`Player <connect4.player.Player>`: The winner.
        """

        winner = None
        current_player = self.player1

        while winner is None and not self.board.is_full():
            print(self.board)
            col = current_player.play(self.board)
            print('Player {0} plays in column {1}.'.format(
                  current_player, col + 1))
            self.board.insert(col, current_player.coin)
            winner = self.check_winner()
            current_player = (self.player1 if current_player == self.player2
                              else self.player2)
            print()

        print(self.board)
        if winner is not None:
            print('Player {0} won the game!'.format(winner))
        else:
            print("There's no winner. You're both LOSERS.")

        return winner
