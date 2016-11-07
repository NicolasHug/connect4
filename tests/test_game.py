"""
This module tests the game class.
"""

import pytest

from connect4 import Game
from connect4 import Board
from connect4 import Player


def test_insert():

    board = Board(10, 10)
    # outside range
    with pytest.raises(ValueError):
        board.insert(-1, 'X')
    with pytest.raises(ValueError):
        board.insert(board.n_cols, 'X')

    for row in range(board.n_rows):
        board.grid[row][0] = 'X'

    # insert in full column
    with pytest.raises(ValueError):
        board.insert(0, 'X')


def test_board_is_full():

    board = Board(10, 10)
    assert not board.is_full()
    for i in range(board.n_rows):
        for j in range(board.n_cols):
            board.grid[i][j] = 'X'
    assert board.is_full()


def test_to_win():

    player2 = Player('O')
    g = Game((Player('X'), player2), to_win=1)
    g.board.grid[0][0] = 'O'

    assert g.check_winner() is player2


def test_check_winner():

    n_rows = 20
    n_cols = 10
    to_win = 5
    player1 = Player('X')
    player2 = Player('O')
    g = Game((player1, player2), n_rows=n_rows, n_cols=n_cols,
             to_win=to_win)

    assert g.check_winner() is None

    # check horizontal win
    for col in range(g.to_win):
        g.board.insert(2 + col, 'X')
    assert g.check_winner() is player1

    # check vertical win
    g = Game((player1, player2), n_rows=n_rows, n_cols=n_cols,
             to_win=to_win)
    for _ in range(g.to_win):
        g.board.insert(0, 'O')
    assert g.check_winner() is player2

    # check positive diagonal win
    g = Game((player1, player2), n_rows=n_rows, n_cols=n_cols,
             to_win=to_win)
    for i in range(g.to_win):
        g.board.grid[g.board.n_rows - 1 - i][i] = 'O'
    assert g.check_winner() is player2

    # check negative diagonal win
    g = Game((player1, player2), n_rows=n_rows, n_cols=n_cols,
             to_win=to_win)
    for i in range(g.to_win):
        g.board.grid[i][i] = 'O'
    assert g.check_winner() is player2
