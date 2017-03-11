from AI import *
import random

def RandomPlayer(game):
    return 0, random.choice(game.get_available_moves())

def ABPlayer(game):
    return alpha_beta_search(game, 8, -np.inf, np.inf, True, evaluate_base)

def ABChainPlayer1(game):
    return alpha_beta_search(game, 7, -np.inf, np.inf, True, evaluate_chain_len)

def ABChainPlayer2(game):
    return alpha_beta_search(game, 7, -np.inf, np.inf, True, evaluate_chain_count)


players = [ABChainPlayer2, ABPlayer]
player_names = tuple((map(lambda x: x.__name__, players)))

print "%s v. %s" % player_names
game = DotsAndBoxes(-1, 4, 4)

while not game.is_over():
    play_fn = players[game.turn == 1]
    print "\tTurn: %s" % (player_names[game.turn == 1])
    score, move = play_fn(game)
    game.play(move)
    print "\tPlayed: %d %d" % (move)
    print "\tEvaluated score: %d\n" % (score)

print "Winner: %s" % (player_names[np.argmax(game.score)])
print game.score