import copy
import random
from cards import Card
from player import Player
from state import State
from play import Play

BOARD_PROTOTYPE = []
PLAYERS_PROTOTYPE = {}
NUM_CARDS = 8
CARDS_PER_PLAYER = 3
BRICK_CARDS = 2
BRICK_PREREQ = 5
MONEY_CARDS = 1

class Game():
    def __init__(self):
        pass

    def start(self):
        new_board = copy.copy(BOARD_PROTOTYPE)
        players = copy.copy(PLAYERS_PROTOTYPE)
        deck = []
        card_id = 0
        for j in range(BRICK_CARDS):
            deck.append(Card(card_id, points=0, prereq=None, symbol='B',color='brown'))
            card_id += 1  # TODO: make this better
        for j in range(BRICK_PREREQ):
            deck.append(Card(card_id, points=random.randint(10, 20), prereq='B', symbol=None,color='blue'))
            card_id += 1  # TODO: make this better
        for j in range(MONEY_CARDS):
            deck.append(Card(card_id, points=0, prereq=None, symbol='$',color='yellow'))
            card_id += 1  # TODO: make this better
        while len(deck) < NUM_CARDS:
            deck.append(Card(card_id, points=random.randint(0, 15), prereq=None, symbol=None,color='yellow'))
            card_id += 1 #TODO: make this better
        players[1] = Player(1)
        players[-1] = Player(-1)
        deck = random.sample(deck, k=len(deck))
        for i in range(4):
            new_board.append(deck.pop())
        return State([], new_board, 1, players, deck)

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

    def next_state(self, state, play):
        new_history = copy.deepcopy(state.play_history) #deepcopy?
        new_deck = copy.deepcopy(state.deck)
        new_history.append(play.to_JSON())
        new_board = copy.deepcopy(state.board)
        for card in new_board:
            if card.id == play.card.id:
                new_board.remove(card)
                break
        player_id = play.player_id
        new_player = -state.player
        new_players = copy.deepcopy(state.players)
        if play.type == "play":
            new_players[player_id].cards.append(play.card)
            if play.card.symbol == "$":
                new_players[player_id].money += 6
        elif play.type == "discard":
            new_players[player_id].money += 3 + new_players[player_id].get_num_color_cards('yellow')
        elif play.type == "buy":
            new_players[player_id].cards.append(play.card)
            new_players[player_id].money -= 2
        if len(new_deck) > 0:
            new_board.append(new_deck.pop())
        next_state = State(new_history, new_board, new_player, new_players, new_deck)
        return next_state

    def winner(self, state):
        if len(state.board) > (NUM_CARDS - 2*CARDS_PER_PLAYER):
            return None
        if state.players[1].get_points() > state.players[-1].get_points():
            return 1
        elif state.players[-1].get_points() > state.players[1].get_points():
            return -1
        else:
            return 0
