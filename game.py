import copy
import random
from cards import Card
from player import Player
from state import State
from play import Play
from board import Board

PLAYERS_PROTOTYPE = {}
NUM_CARDS = 9
CARDS_PER_PLAYER = 4
BRICK_CARDS = 2
BRICK_PREREQ = 5
MONEY_CARDS = 1
MILITARY_CARDS = 0
GREEN_CARDS = 0
GREEN_SYMBOLS = ["!","@","#","%"]
SCIENCE_SYMBOLS_VICTORY = 3
MILITARY_DIFFERENCE_VICTORY = 2

class Game():
    def __init__(self, players):
        self.players = players
        self.board = None
        self.deck = None
        self.current_player = None

    def set_up(self):
        self.board = Board()
        self.deck = []
        card_id = 0
        for j in range(BRICK_CARDS):
            self.deck.append(Card(card_id, points=0, prereq=None, symbol='B', color='brown'))
            card_id += 1  # TODO: make this better
        for j in range(BRICK_PREREQ):
            self.deck.append(Card(card_id, points=random.randint(10, 20), prereq='B', symbol=None, color='blue'))
            card_id += 1  # TODO: make this better
        for j in range(MONEY_CARDS):
            self.deck.append(Card(card_id, points=0, prereq=None, symbol='$', color='yellow'))
            card_id += 1  # TODO: make this better
        for j in range(MILITARY_CARDS):
            self.deck.append(Card(card_id, points=0, prereq=None, symbol='X', color='red'))
            card_id += 1  # TODO: make this better
        for j in range(GREEN_CARDS):
            self.deck.append(Card(card_id, points=0, prereq=None, symbol=random.choice(GREEN_SYMBOLS), color='green'))
            card_id += 1  # TODO: make this better
        while len(self.deck) < NUM_CARDS:
            self.deck.append(Card(card_id, points=random.randint(0, 15), prereq=None, symbol=None, color='yellow'))
            card_id += 1  # TODO: make this better
        random.shuffle(self.deck)
        for i in range(len(self.deck)):
            self.board.add_card(self.deck.pop())

    def start(self):
        self.board.make_pyramid(age=1)
        self.current_player = self.players[0]
        #return State([], new_board, 1, players, deck)

    def get_state(self):
        return State([], copy.deepcopy(self.board), self.current_player.get_id(), copy.deepcopy(self.players), copy.deepcopy(self.deck))

    def get_current_player(self):
        return self.current_player

    def get_current_player_id(self):
        return self.current_player.get_id()

    def did_player_win(self, player_id):
        return 1 if self.get_winner_id() == player_id else -100

    def get_possible_moves(self, player=None):
        legal_plays = []
        if player:
            if player.get_id() != self.get_current_player_id():
                return []
        cur_player_id = self.current_player.get_id()
        for card in self.board.get_cards():
            legal_plays.append(Play(cur_player_id, card, type="discard"))
            if card.prereq is None or self.current_player.has_prereq(card.prereq):
                legal_plays.append(Play(cur_player_id, card, type="play"))
            if not self.current_player.has_prereq(card.prereq) and self.current_player.money > 2:
                legal_plays.append(Play(cur_player_id, card, type="buy"))
        return legal_plays

    def apply_state(self, state):
        self.board = state.board
        self.players = state.players
        self.deck = state.deck
        for player in self.players:
            if player.get_id() == state.current_player_id:
                self.current_player = player

    def new_game_from_state(self, state):
        new_game = copy.deepcopy(self)
        new_game.apply_state(state)
        return new_game


    def legal_plays(self, state):
        legal_plays = []
        cur_player_num = state.player
        cur_player = state.players[cur_player_num]
        for card in state.board:
            legal_plays.append(Play(state.player, card, type="discard"))
            if card.prereq is None or cur_player.has_prereq(card.prereq):
                legal_plays.append(Play(state.player, card, type="play"))
            if not cur_player.has_prereq(card.prereq) and cur_player.money > 2:
                legal_plays.append(Play(state.player, card, type="buy"))
        return legal_plays

    def do_move(self, play):
        for card in self.board.get_cards():
            if card.id == play.card.id:
                self.board.remove_card(card)
                break
        player_id = play.player_id
        if player_id != self.current_player.get_id():
            raise Exception("Current Player not playing!")
        if play.type == "play":
            self.current_player.cards.append(play.card)
            if play.card.symbol == "$":
                self.current_player.money += 6
            elif play.card.symbol == "X":
                self.current_player.add_military(1)
        elif play.type == "discard":
            self.current_player.money += 3 + self.current_player.get_num_color_cards('yellow')
        elif play.type == "buy":
            self.current_player.cards.append(play.card)
            self.current_player.money -= 2
        if len(self.deck) > 0:
            self.board.add_card(self.deck.pop())
        self.current_player = self.get_next_player(player_id)
        #next_state = State(new_history, new_board, new_player, new_players, new_deck)
        #return next_state

    def get_next_player(self, player_id):
        next = player_id + 1
        if next == len(self.players):
            next = 0
        return self.players[next]

    def is_over(self):
        #check if anyone has 2 more red cards
        #game over deck = # of cards - cards per player
        if self.get_military_winner() is not None:
            print("MILITARY")
            return True
        if self.get_science_winner() is not None:
        	print ("SCIENCE")
        	return True
        return len(self.deck) + self.board.get_size() == (NUM_CARDS - 2*CARDS_PER_PLAYER)

    def get_winner_id(self):
        military_winner = self.get_military_winner()
        if military_winner is not None:
            return military_winner

        science_winner = self.get_science_winner()
        if science_winner is not None:
            return science_winner

        if self.players[0].get_points() > self.players[1].get_points():
            return self.players[0].get_id()
        elif self.players[1].get_points() > self.players[0].get_points():
            return self.players[1].get_id()
        else:
            return -1

    def get_science_winner(self):
        for player in self.players:
            if player.get_unique_science_symbol_count() >= SCIENCE_SYMBOLS_VICTORY:
                return player.get_id()
        return None

    def get_military_winner(self):
        if self.players[0].military - self.players[1].military >= MILITARY_DIFFERENCE_VICTORY:
            return self.players[0].get_id()
        if self.players[1].military - self.players[0].military >= MILITARY_DIFFERENCE_VICTORY:
            return self.players[1].get_id()
        return None

    def get_winner(self):
        if self.get_winner_id() == self.players[0].get_id():
            return "Player 0"
        elif self.get_winner_id() == self.players[1].get_id():
            return "Player 1"
        else:
            return "None! It's a draw!"
