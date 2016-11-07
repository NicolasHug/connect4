"""
This module contains the :class:`Board` and the :class:`Game` class.
"""

# Note: some (great) implementation ideas were inspired by Patrick Westerhoff:
# https://gist.github.com/poke/6934842

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

    def col_is_free(self, col):
        """Check if one can insert a coin in given column.

        Args:
            col(int): The column

        Returns:
            ``True`` if the column is free, else ``False``.
        """

        return self.grid[0][col] == self.EMPTY

    def is_full(self):
        """Check if the board is full.

        Returns:
            ``True`` if the board is full, else ``False``.
        """

        return all(not self.col_is_free(col) for col in range(self.n_cols))


class Game:
    """A basic implementation of the connect4 game.

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
        self.to_win = to_win
        self.player1, self.player2 = players

        if self.player1.coin == self.player2.coin:
            raise ValueError('Both players have the same coin.')

    def check_winner(self):
        """Check if there's a winner at the current game state.

        Returns:
            :class:`Player <connect4.player.Player>`: The winner.  If no
            player has won yet, ``None`` is returned.
        """

        def diagonals():
            """Generator function to iterate over all the diagonals."""

            start = self.to_win - 1
            end = self.board.n_rows + self.board.n_cols - self.to_win
            pos_diag_indices = (((r - c, c) for c in range(self.board.n_cols))
                                for r in range(start, end))
            start = self.to_win - self.board.n_cols
            end = self.board.n_rows - self.to_win + 1
            neg_diag_indices = (((r + c, c) for c in range(self.board.n_cols))
                                for r in range(start, end))

            for d in chain(pos_diag_indices, neg_diag_indices):
                yield (self.board.grid[i][j] for (i, j) in d
                       if 0 <= i < self.board.n_rows and
                       0 <= j < self.board.n_cols)

        rows = self.board.grid
        columns = zip(*self.board.grid)

        # for every line, column and diag, check if there are 'to_win' pieces
        # of the same color that are aligned. Is so, return the color.
        for sequence in chain(rows, columns, diagonals()):
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
            print()
            print(self)
            col = current_player.play(self.board)
            print('Player {0} plays in column {1}.'.format(
                  current_player, col + 1))
            self.board.insert(col, current_player.coin)
            winner = self.check_winner()
            current_player = (self.player1 if current_player == self.player2
                              else self.player2)

        print(self)
        if winner is not None:
            print('Player {0} won the game!'.format(winner))
        else:
            print("There's no winner. You're both LOSERS.")

        return winner

    def __str__(self):

        s = ' '.join('{0:2s}'.format(str(i + 1))
                     for i in range(self.board.n_cols)) + '\n'
        s += '\n'.join('  '.join(cell for cell in row)
                       for row in self.board.grid)
        return s
