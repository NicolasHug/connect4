"""
This module contains the :class:`Player` class and all derived player classes.
"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import random
from itertools import groupby
try:
    from itertools import zip_longest
except ImportError:
    from itertools import izip_longest as zip_longest  # Python 2


class Player:
    """The Player base class.

    Args:
        coin(str): The coin representing the user.
    """

    def __init__(self, coin):

        self.coin = coin

        # Players (may) need to know their opponent and the number of
        # successive coins needed to win the game.

        self.opponent = None  # will be set by the game
        self.to_win = None  # will be set by the game

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
            found_col = board.is_free(col)

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
                assert board.is_free(col)
                input_ok = True
            except (ValueError, AssertionError):
                print('Invalid choice.')
                pass

        return col


class Minimax(Player):
    """An IA player using the Minimax algorithm (with alpha/beta pruning).

    Args:
        coin(str): The coin representing the user.
        depth: The maximum depth of the minimax algorithm. Default is ``5``.
    """

    def __init__(self, coin, depth=5):

        Player.__init__(self, coin)
        self.depth = depth

    def utility(self, board):
        """The utility function to evaluate the *goodness* of a board for the
        player.

        Right now, the evaluation is as follows:

            - If the player wins, :math:`\infty` is returned.
            - If he loses, :math:`-\infty` is returned.
            - If there is no winner, the utility value starts from :math:`0`
              and inscremented by :math:`l^2` for each sequence of length
              :math:`l` that could lead to a win for the player, and
              decremented by the same amount for each sequence that could lead
              to a win for the opponent.

        Args:
            board(:class:`Board <connect4.game.Board>`): The board to evaluate.

        Returns:
            The estimated utility of the board.
        """

        def pred_current_next(iterable, fill_pred, fill_next):
            """Generator function that will yield each element of the iterable,
            surrounded by it's previous and next element. Default values for
            previous and next need to be assigned.
            """
            pred_elt = fill_pred
            for current_elt, next_elt in zip_longest(iterable, iterable[1:],
                                                     fillvalue=fill_next):
                yield pred_elt, current_elt, next_elt
                pred_elt = current_elt

        h = 0
        for sequence in board.all_sequences(to_win=self.to_win):
            grouped = [(key, list(g)) for (key, g) in groupby(sequence)]

            for ((pred_coin, pred_group),
                 (current_coin, current_group),
                 (next_coin, next_group)) in pred_current_next(
                                             grouped,
                                             fill_pred=(None, []),
                                             fill_next=(None, [])):

                l = len(current_group)
                if l >= self.to_win:
                    if current_coin == self.coin:
                        return float('inf')
                    elif current_coin == self.opponent.coin:
                        return float('-inf')
                else:
                    mul = (pred_coin == '.' and
                           l + len(pred_group) >= self.to_win)
                    mul += (next_coin == '.' and
                            l + len(next_group) >= self.to_win)
                    if current_coin == self.coin:
                        h += mul * l**2
                    elif current_coin == self.opponent.coin:
                        h -= mul * l**2

        # Try to force central playing
        for row in range(1, board.n_rows // 2):
            h += board.grid[-row][board.n_cols // 2] == self.coin

        return h

    def minimax(self, node, depth, alpha, beta):
        """Run the minimax graph exploration procedure on given node, and
        update the node's attributes.

        If the node is a terminal node (max depth is reached, some player wins
        or the board is full), then ``node.score`` is set using the
        :meth:`utility()` function.

        Else, :meth:`minimax` is called for all possible child nodes to compute
        their score. Once done, the current node score is updated (depending on
        the player) and the column that leads to the best score is also set.

        Args:
            node(Node): The current node.
            depth(int): The current depth
            alpha: The best value that player *self* can expect so far.
            beta: The best value that the opponent of player *self* can expect
                so far.
        """

        # Compute utility of current node: if there's a winner, we want to stop
        # the search.
        score = self.utility(node.board)

        # Stop the search if the maximum depth is reached, if there's a winner
        # or if the board is full.
        if (depth == 0 or
            score in (float('-inf'), float('inf')) or
            node.board.is_full()):  # noqa

            node.score = score
            return

        best_child = Node(board=None,
                          player=None,
                          col_played=None,
                          col_to_play=None,
                          score=(float('-inf') if node.player is self
                                 else float('inf')),
                          childs=[])

        # For every possible move
        for col in node.board.free_columns():

            # Build a child node with an updated board. We'll need to delete
            # the coin later as the same board object is shared among all
            # nodes.
            child_board = node.board
            row = child_board.insert(col, node.player.coin)
            child = Node(board=child_board,
                         player=(self.opponent if node.player is self
                                 else self),
                         col_played=col,
                         col_to_play=None,  # will be set later on
                         score=None,  # will be set later on
                         childs=[]  # will be set later on
                         )

            self.minimax(child, depth - 1, alpha, beta)

            # Now delete the child's move from the board
            child_board.grid[row][col] = child_board.EMPTY

            # Update the best_child, alpha, beta and prune if needed.
            if node.player is self:
                best_child = max((best_child, child),
                                 key=lambda x: x.score)
                alpha = max(alpha, best_child.score)
            else:
                best_child = min((best_child, child),
                                 key=lambda x: x.score)
                beta = min(beta, best_child.score)

            if beta <= alpha:
                break

        # And most importantly, set the column to play and the node score.
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
                    player=self,
                    col_played=None,
                    col_to_play=None,
                    score=None,
                    childs=[])
        self.minimax(node, self.depth, alpha=float('-inf'), beta=float('inf'))

        print(node)
        return node.col_to_play


class Node:
    """A node class for the minimax algorithm graph search.

    A node represents a game state.

    Args:
        board(:class:`Board <connect4.game.Board>`): The current board. For
            efficiency purpose, the board is actually shared among all nodes of
            the graph.
        player(:class:`Player`): The current player.
        col_played(int): The column played at the parent node.
        col_to_play(int): The column to play that will result in the best
            outcome.
        score(int): The score of the current game state.
        childs(list): The child nodes.
    """

    def __init__(self, board, player, col_played, col_to_play, score,
                 childs):

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
