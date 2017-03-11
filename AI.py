import sys
from DotsAndBoxes import *

def evaluate(game, player):
    player_score = game.score[player == 1]
    opponent_score = game.score[player == -1]
    return player_score - opponent_score

def copy_play(game, move):
    g = DotsAndBoxes(game_obj=game)
    g.play(move)
    return g

def alpha_beta_search(game, depth, a, b, maximize):
    if depth == 0 or game.is_over():
        return evaluate(game, game.turn), None
    
    if maximize:
        v = -np.inf
        available_moves = game.get_available_moves()
        best_move, best_score = available_moves[0], v
        for move in available_moves:
            g = copy_play(game, move)
            if g.turn == game.turn:
                v = max(v, alpha_beta_search(g, depth - 1, a, b, True)[0])
            else:
                v = max(v, alpha_beta_search(g, depth - 1, a, b, False)[0])
            if v > best_score:
                best_move = move
                best_score = v
            a = max(a, v)
            if b <= a:
                break
        return v, best_move
    else:
        v = np.inf
        available_moves = game.get_available_moves()
        best_move, best_score = available_moves[0], v
        for move in available_moves:
            g = copy_play(game, move)
            if g.turn == game.turn:
                v = min(v, alpha_beta_search(g, depth - 1, a, b, False)[0])
            else:
                v = min(v, alpha_beta_search(g, depth - 1, a, b, True)[0])
            if v < best_score:
                best_move = move
                best_score = v
            b = min(b, v)
            if b <= a:
                break
        return v, best_move

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("Usage: %s <next-player> <board-string>" % (sys.argv[0]))
    else:
        next_player = sys.argv[1]
        board_string = sys.argv[2]
    
    game = DotsAndBoxes(PLAYERS[next_player], board_string=board_string)
    score, move = alpha_beta_search(game, 8, -np.inf, np.inf, True)
    print "%d %d" % (move)
