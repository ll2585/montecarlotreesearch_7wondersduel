import copy
import random
from cards import Card, DECK, AGE_3_PURPLE_CARDS, WONDERS, SCIENCE_TOKENS
from player import Player
from state import State
from play import Play
from board import Board

PLAYERS_PROTOTYPE = {}
NUM_CARDS = 12
CARDS_PER_PLAYER = 4
BRICK_CARDS = 2
BRICK_PREREQ = 2
MONEY_CARDS = 1
MILITARY_CARDS = 4
GREEN_CARDS = 0
GREEN_SYMBOLS = ["!","@","#","%","L"]
SCIENCE_SYMBOLS_VICTORY = 7
MILITARY_DIFFERENCE_VICTORY = 9

class Game():
    def __init__(self, players):
        self.players = players
        self.board = None
        self.deck = None
        self.current_player = None
        self.seen_and_played_card_ids = []
        self.cur_age = -1
        self.picking_who_to_start = False
        self.zombieing = False
        self.killing_card = None
        self.choosing_science = False
        self.science_tokens_to_choose = None
        self.unused_science_tokens = []
        self.science_tokens = []
        self.discarded_cards = []

    def set_up(self):
        self.cur_age = 1
        self.deck = copy.deepcopy(DECK)
        #random.seed(4) #has red in 4th row - unknown if not cheating, known if cheating


    def start(self):
        wonders = copy.deepcopy(WONDERS)
        random.shuffle(wonders)
        for i in range(0,8):
            print(wonders[i])
            if i % 2 == 0:
                self.players[0].add_wonder(wonders[i])
            else:
                self.players[1].add_wonder(wonders[i])
        tokens = copy.deepcopy(SCIENCE_TOKENS)
        random.shuffle(tokens)
        self.science_tokens = tokens[:5]
        self.unused_science_tokens = tokens[5:]
        self.deal_board(self.cur_age)
        self.current_player = self.players[0]

    def get_state(self):
        return State([], copy.deepcopy(self.board), self.current_player.get_id(), copy.deepcopy(self.players), copy.deepcopy(self.deck), copy.deepcopy(self.seen_and_played_card_ids),
                     copy.deepcopy(self.cur_age),
                     copy.deepcopy(self.picking_who_to_start),
                     copy.deepcopy(self.discarded_cards),
                     copy.deepcopy(self.zombieing),
                     copy.deepcopy(self.killing_card),
                     copy.deepcopy(self.choosing_science),
                     copy.deepcopy(self.science_tokens_to_choose),
                     copy.deepcopy(self.science_tokens),
                     copy.deepcopy(self.unused_science_tokens))

    def get_current_player(self):
        return self.current_player

    def get_current_player_id(self):
        return self.current_player.get_id()

    def did_player_win(self, player_id):
        return 1 if self.get_winner_id() == player_id else 0

    def get_possible_moves(self, player=None):
        legal_plays = []
        if self.is_over():
            return legal_plays
        if player:
            if player.get_id() != self.get_current_player_id():
                return []
        cur_player_id = self.current_player.get_id()
        if self.picking_who_to_start:
            legal_plays.append(Play(cur_player_id, None, type="choose_me"))
            legal_plays.append(Play(cur_player_id, None, type="choose_you"))
        elif self.zombieing:
            for card in self.discarded_cards:
                legal_plays.append(Play(cur_player_id, card, type="play_zombie"))
        elif self.killing_card is not None:
            for card in self.current_player.opponent.cards:
                if card.color == self.killing_card:
                    legal_plays.append(Play(cur_player_id, card, type="kill"))
        elif self.choosing_science:
            for token in self.science_tokens_to_choose:
                legal_plays.append(Play(cur_player_id, token, type="pick_science"))
        else:
            for card in self.board.get_cards():
                legal_plays.append(Play(cur_player_id, card, type="discard"))
                if self.current_player.can_build_card(card) or self.current_player.can_chain_card(card):
                    legal_plays.append(Play(cur_player_id, card, type="play"))
                elif self.current_player.can_buy_card(card):
                    legal_plays.append(Play(cur_player_id, card, type="buy"))
                if self.players[0].get_built_wonder_count() + self.players[1].get_built_wonder_count()  < 7:
                    for wonder in self.current_player.get_wonders():
                        if self.current_player.can_build_card(wonder):
                            legal_plays.append(Play(cur_player_id, card, type="build_wonder", wonder=wonder))
                        elif self.current_player.can_buy_card(wonder):
                            legal_plays.append(Play(cur_player_id, card, type="buy_wonder", wonder=wonder))
        return legal_plays

    def player_can_buy_resources(self, player_to_buy, resources): #takes array of resources
        player_money = player_to_buy.money
        total_resource_cost = self.get_resource_cost(player_to_buy, resources)
        return player_money >= total_resource_cost

    def get_resource_cost(self, player_to_buy, resources):
        opponent = self.players[0] if player_to_buy.id == self.players[1].id else self.players[1]
        missing_resources = player_to_buy.missing_resources(resources)
        resource_cost = 2
        total_resource_cost = resource_cost
        for resource in missing_resources:
            if player_to_buy.has_trading_post(resource):
                total_resource_cost += 1
            else:
                opponent_amt = opponent.amt_of_resource(resource)
                total_resource_cost += opponent_amt
        return total_resource_cost

    def apply_state(self, state):
        self.board = state.board
        self.players = state.players
        self.deck = state.deck
        self.seen_and_played_card_ids = state.seen_and_played_card_ids
        self.cur_age = state.cur_age
        self.picking_who_to_start = state.picking_who_to_start
        self.discarded_cards = state.discarded_cards
        self.zombieing = state.zombieing
        self.killing_card = state.killing_card
        self.choosing_science = state.choosing_science
        self.science_tokens_to_choose = state.science_tokens_to_choose
        self.science_tokens = state.science_tokens
        self.unused_science_tokens = state.unused_science_tokens

        for player in self.players:
            if player.get_id() == state.current_player_id:
                self.current_player = player

    def deal_board(self, age):
        self.board = Board()
        age_deck = self.deck[self.cur_age-1]
        random.shuffle(age_deck)
        deck_index = 0
        deck_to_deal = []
        while deck_index < (len(age_deck)-3): #take out 3 cards - add 3 purples in age 3
            deck_to_deal.append(age_deck[deck_index])
            deck_index += 1
        if age == 3:
            guild_cards = random.sample(copy.deepcopy(AGE_3_PURPLE_CARDS), 3)
            deck_to_deal += guild_cards
            random.shuffle(deck_to_deal)
        for card in deck_to_deal:
            self.board.add_card(card)
        self.board.make_pyramid(age=self.cur_age)


    def new_game_from_state(self, state):
        new_game = copy.deepcopy(self)
        new_game.apply_state(state)
        return new_game

    def age_over(self):
        return self.board.is_empty()

    def do_move(self, play):
        player_id = play.player_id
        if player_id != self.current_player.get_id():
            raise Exception("Current Player not playing!")
        if play.type == "choose_me":
            self.current_player = self.current_player
            self.picking_who_to_start = False
        elif play.type == "choose_you":
            self.current_player = self.get_next_player(player_id)
            self.picking_who_to_start = False
        elif play.type == 'pick_science':
            science_token = play.card
            self.current_player.add_science_token(science_token)
            for token in self.science_tokens:
                if token.token_id == science_token.token_id:
                    self.science_tokens.remove(token)
                    break
            self.choosing_science = False
            self.current_player = self.get_next_player(player_id)
            if self.age_over():
                self.cur_age += 1
                if self.cur_age <= 3:
                    self.deal_board(self.cur_age)
                    if self.players[0].get_military() < self.players[1].get_military():
                        self.current_player = self.players[0]
                    elif self.players[1].get_military() < self.players[0].get_military():
                        self.current_player = self.players[1]
                    else:
                        self.current_player = self.current_player
                    self.picking_who_to_start = True
        else:
            for card in self.board.get_cards():
                if card.card_id == play.card.card_id:
                    self.board.remove_card(card)
                    break
            if play.type == "play":
                self.current_player.play_card(play.card)
            elif play.type == "discard":
                self.discarded_cards.append(play.card)
                self.current_player.money += 3 + self.current_player.get_num_color_cards('yellow')
            elif play.type == "buy":
                self.current_player.buy_card(play.card)
            elif play.type == 'build_wonder':
                self.current_player.build_wonder(play.wonder, play.card, by="build")
            elif play.type == 'buy_wonder':
                self.current_player.build_wonder(play.wonder, play.card, by="buy")
            elif play.type == "play_zombie":
                for card in self.discarded_cards:
                    if card.card_id == play.card.card_id:
                        self.discarded_cards.remove(card)
                        break
                self.current_player.play_card(play.card,zombie=True)
                self.zombieing = False
                if self.current_player.has_token(8):
                    go_again = True
            elif play.type == 'kill':
                self.discarded_cards.append(play.card)
                self.current_player.opponent.discard_card(play.card)
                self.killing_card = None
                if self.current_player.has_token(8):
                    go_again = True
            else:
                raise Exception("Wrong play")

            self.seen_and_played_card_ids.append(play.card.card_id)
            go_again = False
            if play.type == 'build_wonder' or play.type == 'buy_wonder':
                if self.current_player.has_token(8):
                    go_again = True
                if play.wonder.symbols is not None:
                    if 2 in play.wonder.symbols:
                        go_again = True
                    if 'zombie' in play.wonder.symbols:
                        self.zombieing = True
                        go_again = True
                    if 'science' in play.wonder.symbols:
                        self.current_player.built_library()
                        go_again = True
                    if 'kill' in play.wonder.symbols:
                        self.killing_card = play.wonder.symbol_additional_info[0]
                        if self.current_player.opponent.get_num_color_cards(self.killing_card) > 0:
                            go_again = True
                        else:
                            self.killing_card = None
            if self.current_player.choose_science and (len(self.science_tokens) > 0 or self.current_player.choose_library_science):
                go_again = True
                if self.current_player.choose_library_science:
                    self.science_tokens_to_choose = self.unused_science_tokens
                else:
                    self.science_tokens_to_choose = self.science_tokens
                self.choosing_science = True
            elif self.age_over():
                self.cur_age += 1
                if self.cur_age <= 3:
                    self.deal_board(self.cur_age)
                    if self.players[0].get_military() < self.players[1].get_military():
                        self.current_player = self.players[0]
                    elif self.players[1].get_military() < self.players[0].get_military():
                        self.current_player = self.players[1]
                    else:
                        self.current_player = self.current_player
                    self.picking_who_to_start = True
            if not self.picking_who_to_start and not go_again:
                self.current_player = self.get_next_player(player_id)

    def get_next_player(self, player_id):
        next = player_id + 1
        if next == len(self.players):
            next = 0
        return self.players[next]

    def is_over(self):
        #check if anyone has 2 more red cards
        #game over deck = # of cards - cards per player
        if self.get_military_winner() is not None:
            return True
        if self.get_science_winner() is not None:
            return True
        return self.board.is_empty() and self.cur_age > 3

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
        if self.players[0].get_military() - self.players[1].get_military() >= MILITARY_DIFFERENCE_VICTORY:
            return self.players[0].get_id()
        if self.players[1].get_military() - self.players[0].get_military() >= MILITARY_DIFFERENCE_VICTORY:
            return self.players[1].get_id()
        return None

    def get_winner(self):
        if self.get_winner_id() == self.players[0].get_id():
            return "Player 0"
        elif self.get_winner_id() == self.players[1].get_id():
            return "Player 1"
        else:
            return "None! It's a draw!"