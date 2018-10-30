from cards import Card, ScienceToken
class DumbGamePlay:
    def __init__(self, player_id, type):
        self.player_id = player_id
        self.type = type

    def hash(self):
        return str(self.to_JSON())

    def to_JSON(self):
        return {'player_id': self.player_id,'type': self.type}

    def __repr__(self):
        return self.hash()