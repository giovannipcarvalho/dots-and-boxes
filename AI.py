import sys
from DotsAndBoxes import *

def longest_chain_from(game, visited, i, j, length):
    place = str(i) + str(j)
    if not (i > 0 and i < game.r and j > 0 and j < game.c) or place in visited:
        return length
    
    visited[place] = True

    # find openings
    horizontal, vertical = game.board[i-1, j] and game.board[i+1, j], game.board[i, j-1] and game.board[i, j+1]

    # follow each opening and return length
    if horizontal:
        return max(longest_chain_from(game, visited, i, j-2, length+1), longest_chain_from(game, visited, i, j+2, length+1))
    elif vertical:
        return max(longest_chain_from(game, visited, i-2, j, length+1), longest_chain_from(game, visited, i+2, j, length+1))

def find_longest_chain(game):
    # for each square in game
    longest_chain = 0
    for i in range(1,game.r,2):
        for j in range(1,game.c,2):
            # find biggest chain starting in square
            longest_chain = max(longest_chain, longest_chain_from(game, dict(), i, j, 0))
    return longest_chain

def get_chain_count(game):
    # for each square in game
    chain_count = 0
    for i in range(1,game.r,2):
        for j in range(1,game.c,2):
            # find biggest chain starting in square
            if longest_chain_from(game, dict(), i, j, 0) >= 3:
                chain_count += 1
    return chain_count

def evaluate_base(game, player):
    player_score = game.score[player == 1]
    opponent_score = game.score[player == -1]
    return player_score - opponent_score

def evaluate_chain_len(game, player):
    player_score = game.score[player == 1]
    opponent_score = game.score[player == -1]
    return player_score - opponent_score - find_longest_chain(game)

def evaluate_chain_count(game, player):
    player_score = game.score[player == 1]
    opponent_score = game.score[player == -1]
    first = 1 if player == -1 else 0
    return player_score - opponent_score - 5*(get_chain_count(game)%2==first)

def copy_play(game, move):
    g = DotsAndBoxes(game_obj=game)
    g.play(move)
    return g

def alpha_beta_search(game, depth, a, b, maximize, evaluate_fn):
    if depth == 0 or game.is_over():
        return evaluate_fn(game, game.turn), None
    
    if maximize:
        v = -np.inf
        available_moves = game.get_available_moves()
        best_move, best_score = available_moves[0], v
        for move in available_moves:
            g = copy_play(game, move)
            if g.turn == game.turn:
                v = max(v, alpha_beta_search(g, depth - 1, a, b, True, evaluate_fn)[0])
            else:
                v = max(v, alpha_beta_search(g, depth - 1, a, b, False, evaluate_fn)[0])
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
                v = min(v, alpha_beta_search(g, depth - 1, a, b, False, evaluate_fn)[0])
            else:
                v = min(v, alpha_beta_search(g, depth - 1, a, b, True, evaluate_fn)[0])
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
    score, move = alpha_beta_search(game, 7, -np.inf, np.inf, True, evaluate_base)
    print "%d %d" % (move)
