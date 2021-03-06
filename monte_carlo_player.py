from dumb_game_player import DumbGamePlayer
from monte_carlo import MonteCarlo
import random

class MonteCarloPlayer(DumbGamePlayer):
    def __init__(self, player_id):
        DumbGamePlayer.__init__(self, player_id)
        self.monte_carlo = None

    def set_game(self, game):
        self.monte_carlo = MonteCarlo(game)

    def move(self):
        move = self.monte_carlo.get_move()
        return move
