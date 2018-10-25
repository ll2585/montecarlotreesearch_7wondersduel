class Play:
    def __init__(self, player_id, card, type):
        self.player_id = player_id
        self.card = card
        self.type = type

    def hash(self):
        card_id = self.card.id
        card_action = self.type
        card_result = self.card.symbol if self.card.symbol is not None else self.card.get_points()
        card_color = self.card.color
        return 'Player {player_id} {card_action} Card {card_id} ({card_result}, {card_color})'.format(
            player_id=self.player_id,
            card_action=card_action,
            card_id=card_id,
            card_result=card_result,
            card_color=card_color
        )

    def to_JSON(self):
        return {'player_id': self.player_id, 'card': self.card.to_JSON(), 'type': self.type}

    def __repr__(self):
        return self.hash()