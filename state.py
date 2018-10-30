import json
import copy
import random
from cards import AGE_1_CARDS

class State:
    def __init__(self, play_history, board, current_player_id, players, deck, seen_and_played_card_ids, cur_age, picking_who_to_start, discarded_cards,
                 zombieing, killing_card, choosing_science, science_tokens_to_choose, science_tokens):
        self.play_history = play_history
        self.board = board
        self.current_player_id = current_player_id
        self.players = players
        self.deck = deck
        self.seen_and_played_card_ids = seen_and_played_card_ids
        self.cur_age = cur_age
        self.picking_who_to_start = picking_who_to_start
        self.discarded_cards = discarded_cards
        self.zombieing = zombieing
        self.killing_card = killing_card
        self.choosing_science = choosing_science
        self.science_tokens_to_choose = science_tokens_to_choose
        self.science_tokens = science_tokens

    def is_player(self, player):
        return self.current_player_id == player

    def hash(self):
        return json.dumps(self.play_history)

    def clone_and_randomize(self, observer):
        #should do unseen and seen cards and deal it out but fuck it
        cloned_state = copy.deepcopy(self)
        cheat = False
        if not cheat:
            full_deck = copy.deepcopy(cloned_state.deck)
            age_deck = full_deck[copy.deepcopy(self.cur_age)-1]
            visible_card_ids = copy.deepcopy(cloned_state.seen_and_played_card_ids)
            invisible_board_indices = [] #array of #s that indicate the indices of the board with a missing card
            for i, card_node in enumerate(cloned_state.board.get_all_cards()):
                if card_node.is_visible() and not card_node.is_empty():
                    visible_card_ids.append(card_node.card.card_id)
                elif not card_node.is_visible():
                    invisible_board_indices.append(i)
            unplayed_cards = []
            for card in age_deck:
                if card.card_id not in visible_card_ids:
                    unplayed_cards.append(card)
            random.shuffle(unplayed_cards)

            if self.cur_age == 3:
                from cards import AGE_3_PURPLE_CARDS
                all_guild_cards = copy.deepcopy(AGE_3_PURPLE_CARDS)
                unseen_guild_cards = []
                for card in all_guild_cards:
                    if card.card_id not in visible_card_ids:
                        unseen_guild_cards.append(card)
                random.shuffle(unseen_guild_cards)
            unplayed_index = 0

            unplayed_guild_index = 0
            for invisible_index in invisible_board_indices:
                if cloned_state.board.cards[invisible_index].card.is_guild_card():
                    random_unplayed_card = unseen_guild_cards[unplayed_guild_index]
                    unplayed_guild_index += 1
                else:
                    random_unplayed_card = unplayed_cards[unplayed_index]
                    unplayed_index += 1
                cloned_state.board.cards[invisible_index].card = random_unplayed_card
        return cloned_state

    def __repr__(self):
        return str({'cur_player_id': self.current_player_id, 'board': self.board, 'players': self.players})