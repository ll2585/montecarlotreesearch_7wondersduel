from cards import Card, ScienceToken
class Play:
    def __init__(self, player_id, card, type, wonder=None):
        self.player_id = player_id
        self.card = card
        self.type = type
        self.wonder = wonder

    def hash(self):
        if self.card is None:
            return 'Player {player_id} {action}'.format(
                player_id=self.player_id,
                action=self.type
            )
        if type(self.card) is Card:
            card_id = self.card.card_id
            card_result = self.card.symbols[0] if self.card.symbols is not None else self.card.get_points()
            card_color = self.card.color
        elif type(self.card) is ScienceToken:
            card_id = self.card.token_id
            card_result = ''
            card_color = ''
        else:
            raise Exception("NOT A CARD OR A TOKEN")
        card_name = self.card.name if self.wonder is None else self.wonder.name
        card_action = self.type

        discard_text = 'discarded {card_name} '.format(card_name = self.card.name)
        return 'Player {player_id} {card_action} {card_name} ({discard_text}{card_id} {card_result}, {card_color})'.format(
            player_id=self.player_id,
            card_action=card_action,
            discard_text = discard_text if self.wonder is not None else '',
            card_name = card_name,
            card_id=card_id,
            card_result=card_result,
            card_color=card_color
        )

    def to_JSON(self):
        return {'player_id': self.player_id, 'card': self.card.to_JSON(), 'type': self.type}

    def __repr__(self):
        return self.hash()