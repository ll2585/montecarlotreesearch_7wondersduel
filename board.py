import math

class Board:

	def __init__(self):
		#[0]  [1]  [2]  [3]  [4]
		#  [5]  [6]  [7]  [8]
		#card nodes? with left and right, isvisible, card, makevisible
		self.cards = []
		self.playable_cards = []

	def add_card(self, card):
		self.cards.append(CardNode(card))
		self.update_playable_cards()

	def make_pyramid(self, age=1):
		if age == 1:
			for i in range(math.floor(self.get_size()/2)+1):
				if i == 0:
					left = None
				else:
					left = i+4
				if i == math.floor(self.get_size()/2):
					right = None
				else:
					right = i+5
				if left is not None:
					self.cards[i].set_left(self.cards[left])
					self.cards[i+4].set_parent_right(self.cards[i])
				if right is not None:
					self.cards[i].set_right(self.cards[right])
					self.cards[i+5].set_parent_left(self.cards[i])
		self.update_playable_cards()
		print([c.card for c in self.cards if c.is_playable()])

	def get_size(self):
		return len(self.cards)

	def is_empty(self):
		return self.get_size() == 0

	def get_cards(self):
		return self.playable_cards

	def remove_card(self, card):
		for c in self.cards:
			if c.card == card:
				c.clear_parents()
				c.remove_card()
				break
		self.update_playable_cards()

	def update_playable_cards(self):
		self.playable_cards = [c.card for c in self.cards if c.is_playable()]

	def __repr__(self):
		first_row = []
		for card in self.cards:
			if card.parent_left is None and card.parent_right is None:
				first_row.append(card)
		
		first_row_strings = [c.card.id if c.card is not None else " " for c in first_row ]
		second_row = []
		for card in first_row:
			if card.left is not None:
				second_row.append(card.left)
		second_row_strings = [c.card.id if c.card is not None else " " for c in second_row ]
		first_row_string = '   '.join([str(v) for v in first_row_strings])
		second_row_string = '  ' + '   '.join([str(v) for v in second_row_strings])
		result = '\n'.join([first_row_string, second_row_string])
		return result

class CardNode():

	def __init__(self, card, left=None, right=None):
		self.card = card
		self.left = None
		self.right = None
		self.is_visible = False
		self.parent_left = None
		self.parent_right = None

	def set_left(self, left):
		self.left = left

	def set_right(self, right):
		self.right = right

	def clear_right(self):
		if self.right is not None:
			self.right.remove_card()

	def clear_left(self):
		if self.left is not None:
			self.left.remove_card()

	def set_parent_left(self, parent):
		self.parent_left = parent

	def set_parent_right(self, parent):
		self.parent_right = parent

	def clear_parents(self):
		if self.parent_left is not None:
			self.parent_left.clear_right()
		if self.parent_right is not None:
			self.parent_right.clear_left()

	def is_playable(self):
		#probably messed up because of cloning and parents and references
		return self.is_left_empty() and self.is_right_empty() and not self.is_empty()

	def remove_card(self):
		self.card = None

	def is_empty(self):
		return self.card is None

	def is_left_empty(self):
		if self.left is not None:
			return self.left.is_empty()
		return True

	def is_right_empty(self):
		if self.right is not None:
			return self.right.is_empty()
		return True