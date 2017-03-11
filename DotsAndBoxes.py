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
        if board_string is not None: # construct from string
            self._from_string(initial_player, board_string)
        elif game_obj is not None:   # copy constructor
            self._copy(game_obj)
        else:
            self.rows, self.cols = rows, cols
            self.score = [0, 0] # B, W
            self.turn = initial_player
            self.board = np.zeros((2*rows-1, 2*cols-1), dtype=np.int)
            self.r, self.c = self.board.shape
            self._edges = np.reshape([i%2 != j%2 for j in xrange(self.c) for i in xrange(self.r)], (self.r, self.c))
            self.num_boxes = (rows-1) * (cols-1)

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
                    self.score[PLAYERS[s] == 1] += 1

    def _copy(self, game_obj):
        self.__dict__.update(game_obj.__dict__)
        self.board = np.array(game_obj.board)
        self.score = game_obj.score[:]

    def play(self, move=None, i=None, j=None, player=None):
        if not player:
            player = self.turn
        if move is not None:
            i, j = move
        if self._is_valid(player, i, j):
            self.board[i, j] = player
            self._update(player, i, j)
        else:
            raise Exception('Invalid move %d,%d' % (i, j))

    def get_available_moves(self):
        unplayed = np.logical_not(self.board)
        moves = np.where(np.logical_and(unplayed, self._edges))
        return zip(moves[0], moves[1])

    def _is_valid(self, player, i, j):
        return self.turn == player and self.board[i, j] == 0 and i%2 != j%2 and not self.is_over()

    def is_over(self):
        return sum(self.score) == self.num_boxes

    def _update(self, player, i, j):
        vertical = i%2 > j%2
        a = self._check_box(player, i, j-1) if vertical else self._check_box(player, i-1, j)
        b = self._check_box(player, i, j+1) if vertical else self._check_box(player, i+1, j)
        if not (a or b): # did not fill any box
            self.turn *= -1

    def _check_box(self, player, i, j):
        if (i and i < self.r) and (j and j < self.c):
            filled = self.board[i-1, j] and self.board[i+1, j] and self.board[i, j-1] and self.board[i, j+1]
            if filled:
                self.board[i, j] = player
                self.score[player == 1] += 1
            return filled
