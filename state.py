import json
import copy

class State:
    def __init__(self, play_history, board, player, players, deck):
        self.play_history = play_history
        self.board = board
        self.player = player
        self.players = players
        self.deck = deck

    def is_player(self, player):
        return self.player == player

    def hash(self):
        return json.dumps(self.play_history)

    def clone_and_randomize(self):
        cloned_state = copy.deepcopy(self)
        seen_cards = []
        for player in cloned_state.players.values():
            for card in player.cards:
                seen_cards.append(card)
        unseen_cards = [card for card in cloned_state.deck if card not in seen_cards]
        return cloned_state

    def __repr__(self):
        return str({'cur_player': self.player, 'board': self.board, 'players': self.players})