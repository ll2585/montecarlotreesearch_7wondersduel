#'use strict'

from pprint import pprint
from game import Game
from player import Player
from random_player import RandomPlayer
from monte_carlo_player import MonteCarloPlayer

# Setup

player_1 = MonteCarloPlayer(0)
player_2 = RandomPlayer(1)
players = [player_1, player_2]
player_1.set_opponent(player_2)
player_2.set_opponent(player_1)
game = Game(players)
for player in players:
    player.set_game(game)
game.set_up()
game.start()

while not game.is_over():
    pprint(game.board)
    print(game.science_tokens)
    cur_player = game.get_current_player()
    move = cur_player.move()
    print(move)
    game.do_move(move)
    print([card.name for card in game.discarded_cards])
    pprint(game.players)

winner = game.get_winner()
print("winner: {0}".format(winner))
pprint(game.players)
'''
mcts = MonteCarlo(game)



state = game.start()

winner = game.winner(state)

# From initial state, play games until end

while (winner is None):

  print("player: {0}".format(1 if state.player == 1 else 2))

  pprint(state.board )
  mcts.run_search(state, 1)

  stats = mcts.get_stats(state)
  pprint(stats)

  play = mcts.best_play(state, "robust")
  print("chosen play: {play}".format(play=play))

  state = game.next_state(state, play)
  winner = game.winner(state)

print("winner: {0}".format(1 if winner == 1 else 2))
pprint(state.players)
'''