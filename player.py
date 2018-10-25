import math

class Player:
    def __init__(self, player_id):
        self.id = player_id
        self.cards = []
        self.money = 0

    def get_points(self):
        total_points = 0
        for c in self.cards:
            points = c.points
            total_points += points
        total_points += math.floor(self.money / 3)
        return total_points

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
        return str({'player_id': self.id, 'cards': self.cards, 'points': self.get_points(), 'coins': self.money})
