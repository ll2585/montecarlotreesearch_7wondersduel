import random


class Card:
    def __init__(self, card_id, points, prereq, symbol, color):
        self.id = card_id
        self.points = points
        self.prereq = prereq
        self.symbol = symbol
        self.color = color

    def to_JSON(self):
        #return {'card_id': self.id, 'points': self.points, 'other_points': self.other_points}
        return {'card_id': self.id, 'points': self.get_points(), 'symbol': self.symbol, 'prereq': self.prereq, 'color': self.color}

    def __repr__(self):
        return str(self.to_JSON())

    def get_points(self):
        return '{0}'.format(self.points)