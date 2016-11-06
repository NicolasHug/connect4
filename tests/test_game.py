"""
This module tests the game class.
"""

import pytest

from connect4.game import Game


def test_board_dim():

    n_rows = 20
    n_cols = 10
    g = Game(n_rows=n_rows, n_cols=n_cols)

    assert g.n_rows == n_rows
    assert g.n_cols == n_cols
    assert len(g.board) == n_rows
    for row in g.board:
        assert len(row) == n_cols


def test_to_win():

    g = Game(to_win=1)
    g.board[0][0] = 'O'

    assert g.check_winner() == ('O')


def test_insert():

    g = Game()

    # outside range
    with pytest.raises(ValueError):
        g.insert(-1, 'X')
    with pytest.raises(ValueError):
        g.insert(g.n_cols, 'X')

    for row in range(g.n_rows):
        g.board[row][0] = 'X'

    # insert in full column
    with pytest.raises(ValueError):
        g.insert(0, 'X')


def test_check_winner():

    n_rows = 20
    n_cols = 10
    to_win = 5
    g = Game(n_rows=n_rows, n_cols=n_cols, to_win=to_win)

    assert g.check_winner() is None

    # check horizontal win
    for col in range(g.to_win):
        g.insert(2 + col, 'X')
    assert g.check_winner() == 'X'

    # check vertical win
    g = Game(n_rows=n_rows, n_cols=n_cols, to_win=to_win)
    for _ in range(g.to_win):
        g.insert(0, 'O')
    assert g.check_winner() == 'O'

    # check positive diagonal win
    g = Game(n_rows=n_rows, n_cols=n_cols, to_win=to_win)
    for i in range(g.to_win):
        g.board[g.n_rows - 1 - i][i] = 'O'
    assert g.check_winner() == 'O'

    # check negative diagonal win
    g = Game(n_rows=n_rows, n_cols=n_cols, to_win=to_win)
    for i in range(g.to_win):
        g.board[i][i] = 'O'
    assert g.check_winner() == 'O'


def test_board_is_full():

    g = Game()

    assert not g.board_is_full()
    for i in range(g.n_rows):
        for j in range(g.n_cols):
            g.board[i][j] = 'X'
    assert g.board_is_full()
