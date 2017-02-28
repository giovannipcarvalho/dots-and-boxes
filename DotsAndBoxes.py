import numpy as np

PLAYER1 = -1
PLAYER2 = 1

class DotsAndBoxes(object):
    def __init__(self, initial_player, cols, rows):
        self.cols, self.rows = cols, rows
        self.turn = initial_player
        self.board = np.zeros((2*rows-1, 2*cols-1), dtype=np.int)
        self.boxes = self.board[1::2, 1::2]

    def play(self, player, x, y):
        if self._is_valid(player, x, y):
            self.board[x, y] = player
            self._update(player, x, y)
        else:
            raise Exception('Invalid move')

    def _is_valid(self, player, x, y):
        turn = self.turn == player   # is players' turn
        even = x%2 != y%2            # x xor y are even
        free = self.board[x, y] == 0 # edge is not already filled
        return turn and even and free

    def _update(self, player, x, y):
        vertical = x%2 > y%2
        if vertical:
            a = self._check_box(player, x, y-1)
            b = self._check_box(player, x, y+1)
        else:
            a = self._check_box(player, x-1, y)
            b = self._check_box(player, x+1, y)
        if not (a or b):
            self.turn *= -1

    def _check_box(self, player, x, y):
        xvalid = x > 0 and x < 2*self.rows-1
        yvalid = y > 0 and y < 2*self.cols-1
        odd = x%2 == y%2 == 1          # valid box coord
        if xvalid and yvalid and odd:
            filled = np.all(self.board[[x-1, x+1, x, x], [y, y, y-1, y+1]])
            if filled:
                self.board[x, y] = player
                return filled
