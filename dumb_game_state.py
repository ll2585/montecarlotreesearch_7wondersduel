import json
import copy
import random
from cards import AGE_1_CARDS

class DumbGameState:
    def __init__(self, obj):
        self.hash = obj
        print(obj)
        self.current_player_id = self.hash['current_player_id']
        self.turns = self.hash['turns']
        self.players = self.hash['players']

    def hash(self):
        return json.dumps(self.play_history)

    def clone_and_randomize(self, observer):
        #should do unseen and seen cards and deal it out but fuck it
        cloned_state = copy.deepcopy(self)
        return cloned_state

    def __repr__(self):
        return str({'cur_player_id': self.current_player_id, 'board': self.board, 'players': self.players})