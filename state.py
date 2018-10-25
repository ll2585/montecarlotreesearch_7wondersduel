import json

class State:
    def __init__(self, play_history, board, player, players):
        self.play_history = play_history
        self.board = board
        self.player = player
        self.players = players

    def is_player(self, player):
        return self.player == player

    def hash(self):
        return json.dumps(self.play_history)

    def __repr__(self):
        return str({'cur_player': self.player, 'board': self.board, 'players': self.players})