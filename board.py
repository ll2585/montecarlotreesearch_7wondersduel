import math


class Board:
    def __init__(self):
        # age 1
        #                [00]    [01]
        #            [02]    [03]    [04]
        #        [05]    [06]    [07]    [08]
        #    [09]    [10]    [11]    [12]    [13]
        #[14]    [15]    [16]    [17]    [18]    [19]
        # age 2
        # [00]    [01]    [02]    [03]    [04]    [05]
        #     [06]    [07]    [08]    [09]    [10]
        #         [11]    [12]    [13]    [14]
        #             [15]    [16]   [17]
        #                 [18]    [19]
        # card nodes? with left and right, isvisible, card, makevisible
        self.cards = []
        self.playable_cards = []
        self.age = -1

    def add_card(self, card):
        self.cards.append(CardNode(card))
        self.update_playable_cards()

    def make_pyramid(self, age=1):
        self.age = age
        if age == 1:
            #just do second and 4th rows - 1, 3, 5 are visible
            second_row = [2,4]
            fourth_row = [9,13]
            for row in [second_row, fourth_row]:
                first_card = row[0]
                last_card = row[1]
                for i in range(first_card, last_card + 1):
                    if i == first_card:
                        left_parent = None
                    else:
                        left_parent = i - (last_card-first_card+1) #3 for 2nd row, 5 for 4th
                    if i == last_card:
                        right_parent = None
                    else:
                        right_parent = i - (last_card-first_card) #2 for 2nd row, 4 for 4th
                    if right_parent is not None:
                        self.cards[right_parent].set_left(self.cards[i])
                        self.cards[right_parent].set_visibility(True)
                        self.cards[i].set_parent_right(self.cards[right_parent])
                    if left_parent is not None:
                        self.cards[left_parent].set_right(self.cards[i])
                        self.cards[left_parent].set_visibility(True)
                        self.cards[i].set_parent_left(self.cards[left_parent])

                    left = i + (last_card-first_card+1) #3 for 2nd row, 5 for 4th
                    right = i + (last_card-first_card+2) #4 for 2nd row, 6 for 4th

                    self.cards[i].set_left(self.cards[left])
                    self.cards[left].set_visibility(True)
                    self.cards[left].set_parent_right(self.cards[i])

                    self.cards[i].set_right(self.cards[right])
                    self.cards[right].set_visibility(True)
                    self.cards[right].set_parent_left(self.cards[i])
        elif age == 2:
            #first row
            #just do for second row lol
            second_row = [6, 10]
            fourth_row = [15, 17]
            for row in [second_row, fourth_row]:
                first_card = row[0]
                last_card = row[1]
                for i in range(first_card, last_card + 1):
                    left_parent = i - (last_card-first_card+2) #-6 for 2nd row, -4 for 4th
                    right_parent = i - (last_card-first_card+1) #-5 for 2nd row, -3 for 4th

                    self.cards[right_parent].set_left(self.cards[i])
                    self.cards[right_parent].set_visibility(True)
                    self.cards[i].set_parent_right(self.cards[right_parent])

                    self.cards[left_parent].set_right(self.cards[i])
                    self.cards[left_parent].set_visibility(True)
                    self.cards[i].set_parent_left(self.cards[left_parent])

                    if i == first_card:
                        left = None
                    else:
                        left = i + (last_card-first_card) #+4 for 2nd row, +2 for 4th
                    if i == last_card:
                        right = None
                    else:
                        right = i + (last_card-first_card+1) #+5 for 2nd row, +3 for 4th

                    if left is not None:
                        self.cards[i].set_left(self.cards[left])
                        self.cards[left].set_visibility(True)
                        self.cards[left].set_parent_right(self.cards[i])

                    if right is not None:
                        self.cards[i].set_right(self.cards[right])
                        self.cards[right].set_visibility(True)
                        self.cards[right].set_parent_left(self.cards[i])
        elif age == 3:

            #    00  01
            #  02  03  04
            #05  06  07  08
            #  09    10
            #11  12  13  14
            #  15  16  17
            #    18  19
            second_row = [2, 4]
            sixth_row = [15, 17]

            first_card = second_row[0]
            last_card = second_row[1]
            for i in range(first_card, last_card + 1):
                if i == first_card:
                    left_parent = None
                else:
                    left_parent = i - (last_card-first_card+1) #3 for 2nd row, 5 for 4th
                if i == last_card:
                    right_parent = None
                else:
                    right_parent = i - (last_card-first_card) #2 for 2nd row, 4 for 4th
                if right_parent is not None:
                    self.cards[right_parent].set_left(self.cards[i])
                    self.cards[right_parent].set_visibility(True)
                    self.cards[i].set_parent_right(self.cards[right_parent])
                if left_parent is not None:
                    self.cards[left_parent].set_right(self.cards[i])
                    self.cards[left_parent].set_visibility(True)
                    self.cards[i].set_parent_left(self.cards[left_parent])

                left = i + (last_card-first_card+1) #3 for 2nd row, 5 for 4th
                right = i + (last_card-first_card+2) #4 for 2nd row, 6 for 4th

                self.cards[i].set_left(self.cards[left])
                self.cards[left].set_visibility(True)
                self.cards[left].set_parent_right(self.cards[i])

                self.cards[i].set_right(self.cards[right])
                self.cards[right].set_visibility(True)
                self.cards[right].set_parent_left(self.cards[i])
            first_card = sixth_row[0]
            last_card = sixth_row[1]
            for i in range(first_card, last_card + 1):
                left_parent = i - (last_card-first_card+2) #-4 for 4th
                right_parent = i - (last_card-first_card+1) #-3 for 4th

                self.cards[right_parent].set_left(self.cards[i])
                self.cards[right_parent].set_visibility(True)
                self.cards[i].set_parent_right(self.cards[right_parent])

                self.cards[left_parent].set_right(self.cards[i])
                self.cards[left_parent].set_visibility(True)
                self.cards[i].set_parent_left(self.cards[left_parent])

                if i == first_card:
                    left = None
                else:
                    left = i + (last_card-first_card) #+4 for 2nd row, +2 for 4th
                if i == last_card:
                    right = None
                else:
                    right = i + (last_card-first_card+1) #+5 for 2nd row, +3 for 4th

                if left is not None:
                    self.cards[i].set_left(self.cards[left])
                    self.cards[left].set_visibility(True)
                    self.cards[left].set_parent_right(self.cards[i])

                if right is not None:
                    self.cards[i].set_right(self.cards[right])
                    self.cards[right].set_visibility(True)
                    self.cards[right].set_parent_left(self.cards[i])

            # 05  06  07  08
            #   09      10
            # 11  12  13  14
            #only need to set children
            self.cards[9].set_parent_left(self.cards[5])
            self.cards[5].set_right(self.cards[9])
            self.cards[9].set_parent_right(self.cards[6])
            self.cards[6].set_left(self.cards[9])
            self.cards[9].set_left(self.cards[11])
            self.cards[11].set_parent_right(self.cards[9])
            self.cards[9].set_right(self.cards[12])
            self.cards[12].set_parent_left(self.cards[9])

            self.cards[10].set_parent_left(self.cards[7])
            self.cards[7].set_right(self.cards[10])
            self.cards[10].set_parent_right(self.cards[8])
            self.cards[8].set_left(self.cards[10])
            self.cards[10].set_left(self.cards[13])
            self.cards[13].set_parent_right(self.cards[10])
            self.cards[10].set_right(self.cards[14])
            self.cards[14].set_parent_left(self.cards[10])


        for card_node in self.cards:
            card_node.update_visibility()
        self.update_playable_cards()


    def get_size(self):
        cards_shown = 0
        for c in self.cards:
            if c.card is not None:
                cards_shown += 1
        return cards_shown

    def is_empty(self):
        return self.get_size() == 0

    def get_cards(self):
        return self.playable_cards

    def get_all_cards(self):
        return self.cards

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
        #so far for age 1
        first_row = []
        for card in self.cards:
            if card.parent_left is None and card.parent_right is None:
                first_row.append(card)
        first_row_strings = []

        second_row = []
        third_row = []
        fourth_row = []
        fifth_row = []
        sixth_row = []
        seventh_row = []
        rows = [first_row, second_row, third_row, fourth_row, fifth_row, sixth_row, seventh_row]
        for i, row in enumerate(rows):
            if i != len(rows)-1:
                next_row = rows[i+1]
                for card in row:
                    left_card = card.left
                    right_card = card.right
                    if left_card is not None and left_card not in next_row:
                        next_row.append(left_card)
                    if right_card is not None and right_card not in next_row:
                        next_row.append(right_card)
        second_row_strings = []
        third_row_strings = []
        fourth_row_strings = []
        fifth_row_strings = []
        sixth_row_strings = []
        seventh_row_strings = []
        string_mapping = [[first_row, first_row_strings],
                          [second_row, second_row_strings],
                          [third_row, third_row_strings],
                          [fourth_row, fourth_row_strings],
                          [fifth_row, fifth_row_strings],
                          [sixth_row, sixth_row_strings],
                          [seventh_row, seventh_row_strings]]
        for row, strings in string_mapping:
            for c in row:
                val = "   "
                if c.card is not None:
                    if c.is_visible():
                        val = c.card.get_representation()
                    else:
                        val = "???"
                strings.append(val)
        if self.age == 1:
            first_row_string = '   '*4+'   '.join([str(v) for v in first_row_strings])
            second_row_string = '   '*3 + '   '.join([str(v) for v in second_row_strings])
            third_row_string = '   '*2 + '   '.join([str(v) for v in third_row_strings])
            fourth_row_string = '   ' * 1 + '   '.join([str(v) for v in fourth_row_strings])
            fifth_row_string = '   ' * 0 + '   '.join([str(v) for v in fifth_row_strings])
            sixth_row_string = ''
            seventh_row_string = ''
        elif self.age == 2:
            first_row_string = '   ' * 0 + '   '.join([str(v) for v in first_row_strings])
            second_row_string = '   ' * 1 + '   '.join([str(v) for v in second_row_strings])
            third_row_string = '   ' * 2 + '   '.join([str(v) for v in third_row_strings])
            fourth_row_string = '   ' * 3 + '   '.join([str(v) for v in fourth_row_strings])
            fifth_row_string = '   ' * 4 + '   '.join([str(v) for v in fifth_row_strings])
            sixth_row_string = ''
            seventh_row_string = ''
        elif self.age == 3:
            first_row_string = '   ' * 2 + '   '.join([str(v) for v in first_row_strings])
            second_row_string = '   ' * 1 + '   '.join([str(v) for v in second_row_strings])
            third_row_string = '   ' * 0 + '   '.join([str(v) for v in third_row_strings])
            fourth_row_string = '   ' * 1 + '      '.join([str(v) for v in fourth_row_strings])
            fifth_row_string = '   ' * 0 + '   '.join([str(v) for v in fifth_row_strings])
            sixth_row_string = '   ' * 1 + '   '.join([str(v) for v in sixth_row_strings])
            seventh_row_string = '   ' * 2 + '   '.join([str(v) for v in seventh_row_strings])
        result = '\n'.join([first_row_string, second_row_string, third_row_string,fourth_row_string,fifth_row_string,sixth_row_string,seventh_row_string])
        return result


class CardNode():
    def __init__(self, card, left=None, right=None):
        self.card = card
        self.left = None
        self.right = None
        self.visibility = False
        self.parent_left = None
        self.parent_right = None

    def set_left(self, left):
        self.left = left

    def set_right(self, right):
        self.right = right

    def clear_right(self):
        if self.right is not None:
            self.right.remove_card()
        self.update_visibility()

    def clear_left(self):
        if self.left is not None:
            self.left.remove_card()
        self.update_visibility()

    def update_visibility(self):
        if not self.visibility:
            self.set_visibility(self.is_left_empty() and self.is_right_empty())

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
        # probably messed up because of cloning and parents and references
        return self.is_left_empty() and self.is_right_empty() and not self.is_empty()

    def remove_card(self):
        self.card = None

    def is_empty(self):
        return self.card is None

    def set_visibility(self, visibility):
        self.visibility = visibility

    def is_visible(self):
        return self.visibility

    def is_left_empty(self):
        if self.left is not None:
            return self.left.is_empty()
        return True

    def is_right_empty(self):
        if self.right is not None:
            return self.right.is_empty()
        return True
