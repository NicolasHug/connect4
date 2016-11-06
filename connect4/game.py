"""
This module contains the :class:`Game` class.
"""

# Note: some (great) implementation ideas were inspired by Patrick Westerhoff:
# https://gist.github.com/poke/6934842

from itertools import chain
from itertools import groupby

try:
    input = raw_input
except NameError:
    pass

EMPTY = '.'
YELLOW = 'X'
RED = 'O'


class Game:
    """A basic implementation of the connect4 game.

    Args:
        n_rows(int): The number of rows of the board. Default is ``6``.
        n_cols(int): The number of columns of the board. Default is ``7``.
        to_win(int): The number of aligned pieces required to win the game.
            Default is ``4``.

    Attributes:
        n_rows(int): The number of rows of the board. Default is ``6``.
        n_cols(int): The number of columns of the board. Default is ``7``.
        to_win(int): The number of aligned pieces required to win the game.
        board(list of list): The board, represented as a ``n_rows`` *
            ``n_cols`` matrix.
        """

    def __init__(self, n_rows=6, n_cols=7, to_win=4):

        self.n_rows = n_rows
        self.n_cols = n_cols
        self.to_win = to_win

        self.board = [[EMPTY] * n_cols for _ in range(n_rows)]

    def insert(self, col, piece):
        """Insert a piece in given column.

        Args:
            col(int): The column.
            piece(str): The piece to insert.

        Raises:
            ValueError: if ``col`` is full or is out of range.
        """

        if col < 0 or col >= self.n_cols:
            raise ValueError('Invalid column ' + str(col) + '.')

        try:
            r = next(r for r in range(self.n_rows - 1, -1, -1)
                     if self.board[r][col] == EMPTY)
            self.board[r][col] = piece
        except StopIteration:
            raise ValueError('Column ' + str(col) + ' is already full.')

    def check_winner(self):
        """Check if there's a winner at the current game state.

        Returns:
            The winner. If no player has won yet, ``None`` is returned.
        """

        def diagonals():
            """Generator function to iterate over all the diagonals."""

            start = self.to_win - 1
            end = self.n_rows + self.n_cols - self.to_win
            pos_diag_indices = (((r - c, c) for c in range(self.n_cols))
                                for r in range(start, end))
            start = self.to_win - self.n_cols
            end = self.n_rows - self.to_win + 1
            neg_diag_indices = (((r + c, c) for c in range(self.n_cols))
                                for r in range(start, end))

            for d in chain(pos_diag_indices, neg_diag_indices):
                yield (self.board[i][j] for (i, j) in d
                       if 0 <= i < self.n_rows and 0 <= j < self.n_cols)

        rows = self.board
        columns = zip(*self.board)

        # for every line, column and diag, check if there are 'to_win' pieces
        # of the same color that are aligned. Is so, return the color.
        for sequence in chain(rows, columns, diagonals()):
            for cell_val, group in groupby(sequence):
                if cell_val != EMPTY and len(list(group)) >= self.to_win:
                    return cell_val

        return None

    def board_is_full(self):
        """Check if the board is full.

        Returns:
            ``True`` if the board is full, else ``False``.
        """

        return all(cell != EMPTY for cell in self.board[0])

    def run(self):
        """Run a game session between two human players."""

        winner = None
        current_player = RED

        while winner is None and not self.board_is_full():
            print(self)

            # get column from std input
            input_ok = False
            while not input_ok:
                try:
                    msg = "{0}'s turn. Please choose a column: ".format(
                          'Red' if current_player == RED else 'Yellow')
                    col = int(input(msg)) - 1
                    assert 0 <= col < self.n_cols
                    assert self.board[0][col] == EMPTY
                    input_ok = True
                except (ValueError, AssertionError):
                    print('Invalid choice.')
                    pass

            self.insert(col, current_player)
            winner = self.check_winner()
            current_player = RED if current_player == YELLOW else YELLOW

        print(self)
        if winner is not None:
            print('Player ' + winner + ' won the game!')
        else:
            print("There's no winner. You're both LOSERS.")

        return winner

    def __str__(self):

        s = ' '.join('{0:2s}'.format(str(i + 1))
                     for i in range(self.n_cols)) + '\n'
        s += '\n'.join('  '.join(cell for cell in row) for row in self.board)
        return s
