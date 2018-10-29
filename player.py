import math
import random
import copy

class Player:
    def __init__(self, player_id):
        self.id = player_id
        self.cards = []
        self.money = 7
        self.game = None
        self.resources = {}
        self.opponent = None
        self.wonders = []
        self.built_wonders = 0
        self.invaded = [False, False]
        self.science_tokens = []
        self.science_symbols = {}
        self.choose_science = False

    def set_game(self, game):
        self.game = game

    def add_science_token(self, token):
        self.science_tokens.append(token)
        if token.token_id == 0 or token.token_id == 9:
            self.money += 6
        if token.token_id == 3:
            self.add_science_symbol("L")
        self.choose_science = False

    def has_token(self, token_id):
        for token in self.science_tokens:
            if token.token_id == token_id:
                return True
        return False

    def get_invaded(self, stage):
        if stage == 1:
            if not self.invaded[0]:
                self.invaded[0] = True
                self.lose_coins(2)
        elif stage == 2:
            if not self.invaded[1]:
                self.invaded[1] = True
                self.lose_coins(5)

    def lose_coins(self, amt):
        self.money -= min(amt, self.money)

    def get_wonders(self):
        return self.wonders

    def add_wonder(self, wonder):
        self.wonders.append(wonder)

    def set_opponent(self, opponent):
        self.opponent = opponent

    def discard_card(self, card):
        for c in self.cards:
            if c.card_id == card.card_id:
                self.cards.remove(c)
                break
        if card.color == 'gray' or card.color == 'brown':
            resources = card.symbols
            for resource in resources:
                if resource in self.resources:
                    self.resources[resource] -= 1

    def play_card(self, c, zombie=False):
        card = copy.deepcopy(c)

        if card.coin_cost is not None and not zombie:
            self.money -= card.coin_cost
        if card.color == 'gray' or card.color == 'brown':
            resources = card.symbols
            for resource in resources:
                if resource not in self.resources:
                    self.resources[resource] = 0
                self.resources[resource] += 1
        if card.color == 'red' or card.color == 'wonder':
            if card.symbols is not None:
                if '-' in card.symbols:
                    self.opponent.lose_coins(card.symbol_additional_info)
                if card.color == 'red' and self.has_token(7):
                    card.symbols.append("X")
            if self.get_military() - self.opponent.get_military() >= 6:
                self.opponent.get_invaded(stage=2)
            elif self.get_military() - self.opponent.get_military() >= 3:
                self.opponent.get_invaded(stage=1)
        self.cards.append(card) #add before the yellwos which count it, but after the red which lets you add a sword to it
        if card.color == 'yellow' or card.color == 'wonder':
            if card.symbols is not None:
                if card.symbols[0] == "$":
                    self.money += card.symbol_additional_info
                elif card.symbols[0] == '*':
                    color = card.symbol_additional_info[0]
                    amt_cards = self.get_num_color_cards(color)
                    amt_per = card.symbol_additional_info[1]
                    self.money += amt_cards * amt_per
        if card.color == 'purple':
            if card.symbol_additional_info[0] != 'wonder' and card.symbol_additional_info[0] != '$':
                opponent_card_num = 0
                my_card_num = 0
                for color in card.symbol_additional_info: #has to choose brown AND gray
                    opponent_card_num += self.opponent.get_num_color_cards(color)
                    my_card_num += self.get_num_color_cards(color)
                self.money += max(opponent_card_num, my_card_num)
        if card.color == 'green':
            self.add_science_symbol(card.symbols[0])
            if self.science_symbols[card.symbols[0]] == 1:
                self.choose_science = True
        if not zombie and self.has_token(9):
            if card.chain_prereq is not None:
                for c in self.cards:
                    if c.card_id == card.chain_prereq:
                        print("CHAINED")
                        self.money += 4
                        break

    def get_military(self):
        military = 0
        for card in self.cards:
            if card.symbols is not None and 'X' in card.symbols:
                for symbol in card.symbols:
                    if symbol == 'X':
                        military += 1
        return military

    def build_wonder(self, wonder, card, by=None):
        if by is None:
            raise Exception ("NEED A BY")
        for w in self.wonders:
            if w.card_id == wonder.card_id:
                self.wonders.remove(w)
                self.built_wonders += 1
        if by == "buy":
            self.buy_card(wonder)
        elif by == "build":
            self.play_card(wonder)

    def get_built_wonder_count(self):
        return self.built_wonders

    def buy_card(self, card):
        card_cost = self.cards_total_cost(card)
        self.money -= card_cost
        if self.opponent.has_token(2):
            self.opponent.add_money(card_cost)
        self.play_card(card)

    def add_money(self, amt):
        self.money += amt

    def get_id(self):
        return self.id

    def move(self):
        possible_moves = self.game.get_possible_moves(self)
        return random.choice(possible_moves)

    def get_points(self):
        total_points = 0
        card_points = 0
        money_points = 0
        guild_points = 0
        military_points = 0
        science_points = 0

        for c in self.cards:
            if c.color == 'purple':
                if c.symbol_additional_info[0] != '$':
                    opponent_card_num = 0
                    my_card_num = 0
                    for color in c.symbol_additional_info:  # has to choose brown AND gray
                        opponent_card_num += self.opponent.get_num_color_cards(color)
                        my_card_num += self.get_num_color_cards(color)
                    guild_points += max(opponent_card_num, my_card_num)
                else:
                    opponent_money = self.opponent.money
                    guild_points += max(math.floor(opponent_money/3), math.floor(self.money/3))
            points = c.points
            card_points += points
        money_points = math.floor(self.money / 3)
        if self.get_military() - self.opponent.get_military() >= 6:
            military_points = 10
        elif self.get_military() - self.opponent.get_military() >= 3:
            military_points = 5
        elif self.get_military() - self.opponent.get_military() >= 1:
            military_points = 2

        if self.has_token(0):
            science_points += 4
        if self.has_token(6):
            science_points += 7
        if self.has_token(5):
            science_points += 3*len(self.science_tokens)

        total_points = card_points + money_points + guild_points + military_points + science_points
        return total_points

    def can_build_card(self, card):
        card_cost = card.resource_cost
        coin_cost = card.coin_cost
        chain_prereq = card.chain_prereq

        if card_cost is None and coin_cost is None:
            return True



        if coin_cost is None:
            coin_cost = 0
        missing_resources = []

        if card_cost is not None:
            missing_resources = self.missing_resources(card) #array?

        return self.money >= coin_cost and len(missing_resources) == 0

    def cards_total_cost(self, card):
        missing_resources = self.missing_resources(card)  # array?

        total_cost = 0
        for resource in missing_resources:
            total_cost += self.get_resource_cost(resource)
        return total_cost

    def can_chain_card(self, card):
        chain_prereq = card.chain_prereq
        if chain_prereq is not None:
            for c in self.cards:
                if c.card_id == chain_prereq:
                    #print("CHIAN", c.card_id, card.card_id)
                    return True
        return False

    def can_buy_card(self, card):
        card_cost = card.resource_cost
        coin_cost = card.coin_cost

        if card_cost is None and coin_cost is None:
            return True

        if coin_cost is None:
            coin_cost = 0
        elif self.money < coin_cost:
            return False

        total_cost = self.cards_total_cost(card) + coin_cost

        return self.money >= total_cost

    def has_resources(self, resources):
        resource_dict = {}
        for resource in resources:
            if resource not in resource_dict:
                resource_dict[resource] = 0
            resource_dict[resource] += 1
        for resource in resource_dict:
            if resource not in self.resources:
                return False
            if self.resources[resource] < resource_dict[resource]:
                return False
        return True

    def amt_of_resource(self, resource):
        if resource not in self.resources:
            return 0
        return self.resources[resource]

    def missing_resources(self, card): #looks at a cards resources, calcualtes whats missing. removes if have masonry/architecture/caravanssary, etc.
        #returns an array
        resources = card.resource_cost #EG: S S S W W G C P
        resource_dict = {}
        for resource in resources:
            if resource not in resource_dict:
                resource_dict[resource] = 0
            resource_dict[resource] += 1 #-> S: 3 W: 2 G: 1 C: 1 P: 1
        missing_resources_dict = {}
        for resource in resource_dict:
            if resource not in self.resources: #eg if my resource dict is: S: 2, W: 3, G: 1, C: 1
                missing_resources_dict[resource] = resource_dict[resource] #missing: P: 1
            elif self.resources[resource] < resource_dict[resource]:
                amt_missing = resource_dict[resource] - self.resources[resource]
                if resource not in missing_resources_dict:
                    missing_resources_dict[resource] = 0
                missing_resources_dict[resource] += amt_missing #missing: S:1 P: 1
        #TODO: insert masonry/architecture


        if len(missing_resources_dict) == 0:
            return []

        # carvansary
        missing_resource_costs = {}
        for resource in missing_resources_dict:
            missing_resource_costs[resource] = self.get_resource_cost(resource)
        card_cost_tuple = sorted(missing_resource_costs.items(), key=lambda kv: kv[1], reverse=True)
        expensive_resources = [a[0] for a in card_cost_tuple]

        if self.has_token(1) and card.color == "wonder":
            if len(expensive_resources) > 0:
                if missing_resources_dict[expensive_resources[0]] > 0:
                    missing_resources_dict[expensive_resources[0]] -= 1
                    missing_resource_costs = {}
                    for resource in missing_resources_dict:
                        missing_resource_costs[resource] = self.get_resource_cost(resource)
                    card_cost_tuple = sorted(missing_resource_costs.items(), key=lambda kv: kv[1], reverse=True)
                    next_expensive_resources = [a[0] for a in card_cost_tuple]
                if len(next_expensive_resources) > 0:
                    if missing_resources_dict[next_expensive_resources[0]] > 0:
                        missing_resources_dict[next_expensive_resources[0]] -= 1
                        missing_resource_costs = {}
                        for resource in missing_resources_dict:
                            missing_resource_costs[resource] = self.get_resource_cost(resource)
                        card_cost_tuple = sorted(missing_resource_costs.items(), key=lambda kv: kv[1], reverse=True)
                        expensive_resources = [a[0] for a in card_cost_tuple]

        if self.has_token(4) and card.color == "blue":
            if len(expensive_resources) > 0:
                if missing_resources_dict[expensive_resources[0]] > 0:
                    missing_resources_dict[expensive_resources[0]] -= 1
                    missing_resource_costs = {}
                    for resource in missing_resources_dict:
                        missing_resource_costs[resource] = self.get_resource_cost(resource)
                    card_cost_tuple = sorted(missing_resource_costs.items(), key=lambda kv: kv[1], reverse=True)
                    next_expensive_resources = [a[0] for a in card_cost_tuple]
                if len(next_expensive_resources) > 0:
                    if missing_resources_dict[next_expensive_resources[0]] > 0:
                        missing_resources_dict[next_expensive_resources[0]] -= 1
                        missing_resource_costs = {}
                        for resource in missing_resources_dict:
                            missing_resource_costs[resource] = self.get_resource_cost(resource)
                        card_cost_tuple = sorted(missing_resource_costs.items(), key=lambda kv: kv[1], reverse=True)
                        expensive_resources = [a[0] for a in card_cost_tuple]

        for c in self.cards:
            if c.symbols is not None and c.symbols[0] == '+':
                for expensive_resource in expensive_resources:
                    if expensive_resource in c.symbol_additional_info and missing_resources_dict[expensive_resource] > 0:
                        missing_resources_dict[expensive_resource] -= 1
                        break

        missing_resources = []
        for resource in missing_resources_dict:
            missing_resources += resource * missing_resources_dict[resource]

        return missing_resources

    def get_resource_cost(self, resource):
        resource_cost = 2
        total_resource_cost = resource_cost
        if self.has_trading_post(resource):
            total_resource_cost = 1
        else:
            opponent_amt = self.opponent.amt_of_resource(resource)
            total_resource_cost += opponent_amt
        return total_resource_cost

    def get_num_color_cards(self, color):
        cards = 0
        for c in self.cards:
            if c.color == color:
                cards += 1
        return cards

    def add_science_symbol(self, symbol):
        if symbol not in self.science_symbols:
            self.science_symbols[symbol] = 0
        self.science_symbols[symbol] += 1

    def get_unique_science_symbol_count(self):
        return len(self.science_symbols)

    def has_trading_post(self, resource):
        for c in self.cards:
            if c.color == 'yellow' and c.symbols is not None and c.symbols[0] == '1':
                for res in c.symbol_additional_info:
                    if res == resource:
                        return True
        return False

    def __repr__(self):
        return str({'player_id': self.id, 'cards': self.cards, 'points': self.get_points(), 'coins': self.money, 'swords': self.get_military()})
