#'use strict'

from pprint import pprint
from game import Game
from monte_carlo import MonteCarlo

# Setup

game = Game()
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