import numpy as np
from scipy.signal import convolve2d

PLAYER1 = -1
PLAYER2 = 1
box_detector = np.matrix('0 1 0; 1 0 1; 0 1 0')

class DotsAndBoxes(object):
    def __init__(self, initial_player, cols, rows):
        self.cols, self.rows = cols, rows
        self.turn = initial_player
        self.board = np.zeros((2*rows-1, 2*cols-1))
        self.boxes = np.zeros((rows-1, cols-1))
    
    def play(self, player, x, y):
        if self._is_valid(player, x, y):
            self.board[x, y] = player
            self._update()
        else:
            raise Exception('Invalid move')
    
    def _is_valid(self, player, x, y):
        turn = self.turn == player   # is players' turn
        even = x%2 != y%2            # x xor y are even
        free = self.board[x, y] == 0 # edge is not already filled
        
        return turn and even and free
    
    def _update(self):
        old_boxes = self.boxes.astype(bool)
        boxes = self._detect_boxes()
        if np.all(boxes == old_boxes): # no new boxes were filled
            self.turn *= -1            # swap turn
        else:
            # attribute new boxes to current player
            self.boxes[old_boxes != boxes] = self.turn
    
    def _detect_boxes(self):
        return convolve2d(abs(self.board), box_detector, mode='valid')[::2, ::2] == 4