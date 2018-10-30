from player import Player
from monte_carlo import MonteCarlo
import random

class MonteCarloPlayer(Player):
    def __init__(self, player_id):
        Player.__init__(self, player_id)
        self.monte_carlo = None

    def set_game(self, game):
        Player.set_game(self, game)
        self.monte_carlo = MonteCarlo(self.game)

    def move(self):
        move = self.monte_carlo.get_move()
        return move
