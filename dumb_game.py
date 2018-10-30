from dumb_game_state import DumbGameState
from dumb_game_play import DumbGamePlay
import copy

class DumbGame:
    def __init__(self, players):
        self.players = players
        self.board = None
        self.turns = 0
        self.current_player = None

    def set_up(self):
        pass

    def get_possible_moves(self):
        if self.is_over():
            return []
        return [DumbGamePlay(0,'nothing'),DumbGamePlay(0,'lose')]

    def did_player_win(self, player_id):
        return player_id == self.get_winner()

    def get_winner(self):
        if self.turns == 1:
            return 0
        else:
            return 1

    def get_current_player_id(self):
        return self.current_player

    def start(self):
        self.current_player = 0

    def get_current_player(self):
        return self.players[self.current_player]

    def new_game_from_state(self, state):
        new_game = copy.deepcopy(self)
        new_game.apply_state(state)
        return new_game

    def apply_state(self, state):
        self.players = state.players
        self.turns = state.turns
        self.current_player = state.current_player_id

    def do_move(self, move):
        if move.type == 'lose':
            self.turns += 2
        else:
            self.turns += 1

    def make_state(self):
        return {
            'players': self.players,
            'turns': self.turns,
            'current_player_id': self.current_player
        }

    def get_state(self):
        return DumbGameState(self.make_state())

    def is_over(self):
        return self.turns > 0