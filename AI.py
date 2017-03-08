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
    player_score = game.score[player == 1]
    opponent_score = game.score[player == -1]
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

def copy_play(game, move):
    g = DotsAndBoxes(game_obj=game)
    g.play(move)
    return g

def alpha_beta(game, max_depth=4):
    def calc_value(game, alpha, beta, depth, maximize):
        if should_stop(game, depth):
            return evaluate(game, game.turn)
        v = -np.inf if maximize else np.inf
        for move in game.get_available_moves():
            g = copy_play(game, move)
            scored = g.turn == game.turn
            if scored:
                v = max(v, calc_value(g, alpha, beta, depth+1, True)) if maximize else min(v, calc_value(g, alpha, beta, depth+1, False))
            else:
                v = max(v, calc_value(g, alpha, beta, depth+1, False)) if maximize else min(v, calc_value(g, alpha, beta, depth+1, True))
            
            if maximize:
                alpha = max(alpha, v)
            else:
                beta = min(beta, v)
            
            if beta <= alpha:
                break
        
        return v
    
    def max_value(game, alpha, beta, depth):
        if should_stop(game, depth):
            return evaluate(game, game.turn)
        v = -np.inf
        for move in game.get_available_moves():
            g = copy_play(game, move)
            scored = g.turn == game.turn
            if scored:
                v = max(v, max_value(g, alpha, beta, depth+1))
            else:
                v = max(v, min_value(g, alpha, beta, depth+1))
            alpha = max(alpha, v)
            if beta <= alpha:
                break
        return v
    
    def min_value(game, alpha, beta, depth):
        if should_stop(game, depth):
            return evaluate(game, game.turn)
        v = np.inf
        for move in game.get_available_moves():
            g = copy_play(game, move)
            scored = g.turn == game.turn
            if scored:
                v = min(v, min_value(g, alpha, beta, depth+1))
            else:
                v = min(v, max_value(g, alpha, beta, depth+1))
            beta = min(beta, v)
            if beta <= alpha:
                break
        return v
    
    should_stop = lambda game, depth: depth >= max_depth or game.is_over()
    
    moves = game.get_available_moves()

    scores = map(lambda m: calc_value(copy_play(game, m), -np.inf, np.inf, 0, True), moves)
    
    return moves[np.argmax(scores)]

if __name__ == "__main__":
    if len(sys.argv) < 3:
        next_player = 'B'
        board_string = '._.x.|_*x*_|.x._.|xBx*_|.x._.'
        # sys.exit("Usage: %s <next-player> <board-string>" % (sys.argv[0]))
    else:
        next_player = sys.argv[1]
        board_string = sys.argv[2]
    
    # game = DotsAndBoxes(PLAYERS[next_player], board_string=board_string)
    game = DotsAndBoxes(-1, 3, 3)
    # print game.board

    # print mini_max(game)
    print alpha_beta(game, 0)
