import json
import copy
import random

class State:
    def __init__(self, play_history, board, current_player_id, players, deck):
        self.play_history = play_history
        self.board = board
        self.current_player_id = current_player_id
        self.players = players
        self.deck = deck

    def is_player(self, player):
        return self.current_player_id == player

    def hash(self):
        return json.dumps(self.play_history)

    def clone_and_randomize(self, observer):
        #should do unseen and seen cards and deal it out but fuck it
        cloned_state = copy.deepcopy(self)
        random.shuffle(cloned_state.deck)
        return cloned_state

    def __repr__(self):
        return str({'cur_player_id': self.current_player_id, 'board': self.board, 'players': self.players})