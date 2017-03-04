import sys
from DotsAndBoxes import *

class Node(object):
    def __init__(self, game=None, score=0, max=True, a=-np.inf, b=np.inf):
        self.game = game
        self.score = score
        self.max = max
        self.a = a
        self.b = b

def evaluate(game, player):
    player_score = np.sum(game.boxes == player)
    opponent_score = np.sum(game.boxes == -player)
    return player_score - opponent_score

def min_play(game):
    if game.is_over():
        return evaluate(game, game.turn)
    moves = game.get_available_moves()
    best_score = np.inf
    for move in moves:
        g = DotsAndBoxes(game_obj=game)
        g.play(move)
        if g.turn == game.turn: # keeps playing
            score = min_play(g) # minimize again
        else:
            score = max_play(g)
        if score < best_score:
            best_move = move
            best_score = score
    return best_score

def max_play(game):
    if game.is_over():
        return evaluate(game, game.turn)
    moves = game.get_available_moves()
    best_score = -np.inf
    for move in moves:
        g = DotsAndBoxes(game_obj=game)
        g.play(move)
        if g.turn == game.turn: # keeps playing
            score = max_play(g) # maximize again
        else:
            score = min_play(g)
        if score > best_score:
            best_move = move
            best_score = score
    return best_score

def mini_max(game):
    moves = game.get_available_moves()
    best_move = moves[0]
    best_score = -np.inf
    for move in moves:
        g = DotsAndBoxes(game_obj=game)
        g.play(move)
        if g.turn == game.turn: # keeps playing
            score = max_play(g) # maximize again
        else:
            score = min_play(g)
        if score > best_score:
            best_move = move
            best_score = score
    return best_move

def alpha_beta(game, max, a, b):
    pass

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("Usage: %s <next-player> <board-string>" % (sys.argv[0]))

    # game = DotsAndBoxes(PLAYER1, board_string='._.x.|_*x*_|.x._.|xBx*_|.x._.')

    next_player = sys.argv[1]
    board_string = sys.argv[2]
    game = DotsAndBoxes(PLAYERS[next_player], board_string=board_string)

    print game.board

    print mini_max(game)