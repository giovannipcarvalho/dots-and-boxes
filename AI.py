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
        return evaluate(game, game.turn)
    
    if maximize:
        v = -np.inf
        for move in game.get_available_moves():
            g = copy_play(game, move)
            if g.turn == game.turn:
                v = max(v, alpha_beta_search(g, depth - 1, a, b, True))
            else:
                v = max(v, alpha_beta_search(g, depth - 1, a, b, False))
            a = max(a, v)
            if b <= a:
                break
        return v
    else:
        v = np.inf
        for move in game.get_available_moves():
            g = copy_play(game, move)
            if g.turn == game.turn:
                v = min(v, alpha_beta_search(g, depth - 1, a, b, False))
            else:
                v = min(v, alpha_beta_search(g, depth - 1, a, b, True))
            b = min(b, v)
            if b <= a:
                break
        return v

if __name__ == "__main__":
    if len(sys.argv) < 3:
        next_player = 'B'
        board_string = '._.x.|_*x*_|.x._.|xBx*_|.x._.'
        # sys.exit("Usage: %s <next-player> <board-string>" % (sys.argv[0]))
    else:
        next_player = sys.argv[1]
        board_string = sys.argv[2]
    
    # game = DotsAndBoxes(PLAYERS[next_player], board_string=board_string)
    game = DotsAndBoxes(-1, 4, 4)
    print alpha_beta_search(game, 8, -np.inf, np.inf, True)
    # moves = game.get_available_moves()
    # scores = map(lambda m: alpha_beta_search(copy_play(game, m), 5, -np.inf, np.inf, True), moves)

    # print game.board

    # print mini_max(game)
    # print alpha_beta(game, 5)
