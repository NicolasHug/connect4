"""
This module contains the :class:`Player` class.
"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import random
from copy import deepcopy
from itertools import chain
from itertools import groupby
from itertools import zip_longest


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


class Minimax(Player):
    """An IA player using the Minimax algorithm.

    Args:
        coin(str): The coin representing the user.
    """

    def __init__(self, coin, depth=5):

        Player.__init__(self, coin)
        #TODO: this supposes there are only two possible coins
        self.coins = {'max': self.coin,
                      'min': 'X' if self.coin == 'O' else 'O'
                      }
        self.depth = depth
        self.opnt_coin = self.coins['min']


    def utility(self, board):

        #TODO: shitty as hell
        to_win = 4

        rows = board.grid
        columns = zip(*board.grid)

        h = 0
        #print('-------')
        #print('-------')
        #print('-------')
        #print('-------')
        #print(board)
        for sequence in board.all_sequences(to_win=to_win):
            pred_coin, pred_group = None, []
            grouped = [(key, list(g)) for (key, g) in groupby(sequence)]
            #print('-------')
            #print(sequence)

            for (cell_coin, group), (next_coin, next_group) in zip_longest(grouped,
                    grouped[1:], fillvalue=(None, [])):
                #print(group, pred_coin, next_coin)
                l = len(group)
                if l >= to_win:
                    if cell_coin == self.coin:
                        return 10000
                    if cell_coin == self.opnt_coin:
                        return -10000
                else:
                    mul = pred_coin == '.' and l + len(pred_group) >= to_win
                    mul += next_coin == '.' and l + len(next_group) >= to_win
                    if cell_coin == self.coin:
                        h += mul * l**2
                    if cell_coin == self.opnt_coin:
                        h -= mul * l**2


                pred_coin, pred_group = cell_coin, group
            #print('h =', h)
        # force central playing at first
        #for row in range(1, board.n_rows // 2):
        #    h += board.grid[-row][board.n_cols // 2] == self.coin

        #print('final h =', h)



        #print(h)
        return h

    def minimax(self, node, depth):

        node.score = self.utility(node.board)

        if depth == 0 or node.score in (10000, -10000):
            return

        for col in range(node.board.n_cols):
            if node.board.col_is_free(col):
                child_board = deepcopy(node.board)
                child_board.insert(col, self.coins[node.player])
                child = Node(board=child_board,
                             player=('min' if node.player == 'max' else
                                     'max'),
                             col_to_play=None,
                             col_played=col,
                             score=None,
                             childs=[])
                node.childs.append(child)

        if not node.childs: return


        for child in node.childs:
            self.minimax(child, depth - 1)

        if node.player == 'max':
            best_child = max((child for child in node.childs),
                             key=lambda x : x.score)
        else:
            best_child = min((child for child in node.childs),
                             key=lambda x : x.score)
        node.col_to_play = best_child.col_played
        node.score = best_child.score

    def play(self, board):
        """Choose a column to play on based on the minimax algorithm.

        Args:
            board(:class:`Board <connect4.game.Board>`): The current board.

        Returns:
            (int): The column to play on.
        """

        node = Node(board=board,
                    player='max',
                    col_to_play=None,
                    col_played=None,
                    score=None,
                    childs=[])
        self.minimax(node, self.depth)

        print(node)
        return node.col_to_play


class Node:

    def __init__(self, board, player, col_to_play, col_played, score, childs):

        self.board = board
        self.player = player
        self.col_to_play = col_to_play
        self.col_played = col_played
        self.score = score
        self.childs = childs

    def __str__(self):
        return '\n'.join(['col_to_play = ' + str(self.col_to_play),
                          'col_played = ' + str(self.col_played),
                          'score = ' + str(self.score),
                          'n_chids = ' + str(len(self.childs))])
