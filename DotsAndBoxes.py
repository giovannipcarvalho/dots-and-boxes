import numpy as np

PLAYER1 = -1
PLAYER2 = 1
PLAYERS = {'B': -1, 'W': 1}

def board_shape(board_string):
    lines = board_string.split("|")
    rows, cols = (len(lines)+1)/2, (len(lines[0])+1)/2
    return rows, cols

class DotsAndBoxes(object):
    def __init__(self, initial_player=None, rows=None, cols=None, board_string=None, game_obj=None):
        if isinstance(board_string, str):      # construct from string
            self._from_string(initial_player, board_string)
        elif isinstance(game_obj, DotsAndBoxes):  # copy constructor
            self._copy(game_obj)
        else:
            self.rows, self.cols = rows, cols
        self.turn = initial_player
        self.board = np.zeros((2*rows-1, 2*cols-1), dtype=np.int)
            self.boxes = self.board[1::2, 1::2]
            r, c = self.board.shape
            self._edges = np.reshape([i%2 != j%2 for j in range(c) for i in range(r)], (r, c))

    def _from_string(self, initial_player, board_string):
        lines = board_string.split("|")
        rows, cols = board_shape(board_string)
        self.__init__(initial_player, rows, cols)
        for i, r in enumerate(lines):
            for j, s in enumerate(r):
                edge, box = i%2 != j%2, i%2 == j%2 == 1
                if edge and s == 'x':      # is a filled edge
                    self.board[i, j] += 1
                elif box and s in PLAYERS: # is a filled box
                    self.board[i, j] = PLAYERS[s]

    def _copy(self, game_obj):
        self.__dict__.update(game_obj.__dict__)
        self.board = np.array(game_obj.board)
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
