import math
import random
import copy

class DumbGamePlayer:
    def __init__(self, player_id):
        self.id = player_id
        self.opponent = None
        self.game = None

    def set_game(self, game):
        self.game = game

    def set_opponent(self, opponent):
        self.opponent = opponent

    def move(self):
        possible_moves = self.game.get_possible_moves(self)
        return random.choice(possible_moves)



    def __repr__(self):
        return str({'player_id': self.id})
