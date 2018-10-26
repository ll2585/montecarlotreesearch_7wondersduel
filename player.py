import math
import random


class Player:
    def __init__(self, player_id):
        self.id = player_id
        self.cards = []
        self.money = 0
        self.game = None
        self.military = 0

    def set_game(self, game):
        self.game = game

    def get_id(self):
        return self.id

    def move(self):
        possible_moves = self.game.get_possible_moves(self)
        return random.choice(possible_moves)

    def get_points(self):
        total_points = 0
        for c in self.cards:
            points = c.points
            total_points += points
        total_points += math.floor(self.money / 3)
        return total_points

    def add_military(self, swords):
        self.military += swords

    def has_prereq(self, prereq):
        for c in self.cards:
            if c.symbol == prereq:
                return True
        return False

    def get_num_color_cards(self, color):
        cards = 0
        for c in self.cards:
            if c.color == color:
                cards += 1
        return cards

    def __repr__(self):
        return str({'player_id': self.id, 'cards': self.cards, 'points': self.get_points(), 'coins': self.money, 'swords': self.military})
