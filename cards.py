COLOR_MAPPING = {
    'brown': "Br",
    'blue': "Bl",
    'red': "Rd",
    'green': "Gn",
    'yellow': "Ye",
    'gray': "Gr",
    'purple': "Pr",
    'wonder': "Wd"
}

class Card:
    def __init__(self, card_id, name, color, age, symbols=None, points=0, resource_cost=None, coin_cost=0,chain_prereq = None, symbol_additional_info = None):
        self.card_id = card_id
        self.name = name
        self.points = points
        self.age = age
        self.resource_cost = resource_cost
        self.symbols = symbols
        self.color = color
        self.coin_cost = coin_cost
        self.chain_prereq = chain_prereq
        self.symbol_additional_info = symbol_additional_info

    def is_guild_card(self):
        return self.color == 'purple'

    def __repr__(self):
        color_part = COLOR_MAPPING[self.color]
        return "{0}-{1}".format(color_part, self.name)

    def get_representation(self):
        return self.card_id

    def get_points(self):
        return '{0}'.format(self.points)

AGE_1_BROWN_CARDS = [
    Card(0, 'CLAY POOL', 'brown', 1, symbols=['C']),
    Card(1, 'CLAY PIT', 'brown', 1, symbols=['C'], coin_cost=1),
    Card(2, 'QUARRY', 'brown', 1, symbols=['S']),
    Card(3, 'STONE PIT', 'brown', 1, symbols=['S'], coin_cost=1),
    Card(4, 'LUMBER YARD', 'brown', 1, symbols=['W']),
    Card(5, 'LOGGING CAMP', 'brown', 1, symbols=['W'], coin_cost=1)
    ]
AGE_1_GRAY_CARDS = [
    Card(6, 'GLASSWORKS', 'gray', 1, symbols=['G'], coin_cost=1),
    Card(7, 'PRESS', 'gray', 1, symbols=['P'], coin_cost=1),
    ]
AGE_1_RED_CARDS = [
    Card(8, 'GUARD TOWER', 'red', 1, symbols=['X']),
    Card(9, 'PALISADE', 'red', 1, symbols=['X'], coin_cost=2),
    Card(10, 'GARRISON', 'red', 1, symbols=['X'], resource_cost=['C']),
    Card(11, 'STABLE', 'red', 1, symbols=['X'], resource_cost=['W']),
    ]
AGE_1_BLUE_CARDS = [
    Card(12, 'ALTAR', 'blue', 1, points=3),
    Card(13, 'THEATER', 'blue', 1, points=3),
    Card(14, 'BATHS', 'blue', 1, points=3, resource_cost=['S'])
    ]
AGE_1_YELLOW_CARDS = [
    Card(15, 'TAVERN', 'yellow', 1, symbols=['$'], symbol_additional_info=4),
    Card(16, 'WOOD RESERVE', 'yellow', 1, symbols=['1'], coin_cost=3, symbol_additional_info=["W"]),
    Card(17, 'STONE RESERVE', 'yellow', 1, symbols=['1'], coin_cost=3, symbol_additional_info=["S"]),
    Card(18, 'CLAY RESERVE', 'yellow', 1, symbols=['1'], coin_cost=3, symbol_additional_info=["C"]),
    ]
AGE_1_GREEN_CARDS = [
    Card(19, 'WORKSHOP', 'green', 1, symbols=['^'], points=1, resource_cost=['P']),
    Card(20, 'APOTHECARY', 'green', 1, symbols=['@'], points=1, resource_cost=['G']),
    Card(21, 'PHARMACIST', 'green', 1, symbols=['#'], coin_cost=2),
    Card(22, 'SCRIPTORIUM', 'green', 1, symbols=['~'], coin_cost=2)
    ]

AGE_1_CARDS =  AGE_1_BROWN_CARDS + \
               AGE_1_GRAY_CARDS + \
               AGE_1_RED_CARDS + \
               AGE_1_BLUE_CARDS + \
               AGE_1_YELLOW_CARDS + \
               AGE_1_GREEN_CARDS

AGE_2_BROWN_CARDS = [
    Card(100, 'SAWMILL', 'brown', 2, symbols=['W','W'], coin_cost=2),
    Card(101, 'BRICKYARD', 'brown', 2, symbols=['C','C'], coin_cost=2),
    Card(102, 'SHELF QUARRY', 'brown', 2, symbols=['S','S'], coin_cost=2),
    ]
AGE_2_GRAY_CARDS = [
    Card(103, 'GLASSBLOWER', 'gray', 2, symbols=['G']),
    Card(104, 'DRYING ROOM', 'gray', 2, symbols=['P']),
    ]
AGE_2_RED_CARDS = [
    Card(105, 'WALLS', 'red', 2, symbols=['X','X'],resource_cost=['S','S']),
    Card(106, 'HORSE BREEDERS', 'red', 2, symbols=['X'], resource_cost=['C','W'], chain_prereq=11),
    Card(107, 'BARRACKS', 'red', 2, symbols=['X'], coin_cost=3, chain_prereq=10),
    Card(108, 'ARCHERY RANGE', 'red', 2, symbols=['X','X'], resource_cost=['S','W','P']),
    Card(109, 'PARADE GROUND', 'red', 2, symbols=['X','X'], resource_cost=['B','B','G']),
    ]
AGE_2_BLUE_CARDS = [
    Card(110, 'COURTHOUSE', 'blue', 2, points=5, resource_cost=['W','W','G']),
    Card(111, 'STATUE', 'blue', 2, points=4, resource_cost=['C','C'],chain_prereq=13),
    Card(112, 'TEMPLE', 'blue', 2, points=4, resource_cost=['W','P'], chain_prereq=12),
    Card(113, 'AQUEDUCT', 'blue', 2, points=5, resource_cost=['S','S','S'], chain_prereq=14),
    Card(114, 'ROSTRUM', 'blue', 2, points=4, resource_cost=['S','W'])
    ]
AGE_2_YELLOW_CARDS = [
    Card(115, 'FORUM', 'yellow', 2, resource_cost=['C'], coin_cost=3, symbols=["+"], symbol_additional_info=['G','P']),
    Card(116, 'CARAVANSERY', 'yellow', 2, resource_cost=['G','P'], coin_cost=2, symbols=["+"], symbol_additional_info=['W','C','S']),
    Card(117, 'CUSTOMS HOUSE', 'yellow', 2, symbols=['1'], symbol_additional_info=["P","G"], coin_cost=4),
    Card(118, 'BREWERY', 'yellow', 2, symbols=['$'], symbol_additional_info=6),
    ]
AGE_2_GREEN_CARDS = [
    Card(119, 'LIBRARY', 'green', 2, symbols=['~'], points=2, resource_cost=['S','W','G'], chain_prereq=22),
    Card(120, 'DISPENSARY', 'green', 2, symbols=['#'], points=2, resource_cost=['C','C','S'], chain_prereq=21),
    Card(121, 'SCHOOL', 'green', 2, symbols=['@'], points=1, resource_cost=['W','P','P']),
    Card(122, 'LABORATORY', 'green', 2, symbols=['^'], points=1, resource_cost=['W','G','G'])
    ]

AGE_2_CARDS =  AGE_2_BROWN_CARDS + \
               AGE_2_GRAY_CARDS + \
               AGE_2_RED_CARDS + \
               AGE_2_BLUE_CARDS + \
               AGE_2_YELLOW_CARDS + \
               AGE_2_GREEN_CARDS

AGE_3_RED_CARDS = [
    Card(1000, 'ARSENAL', 'red', 3, symbols=['X','X','X'],resource_cost=['C','C','C','W','W']),
    Card(1001, 'PRETORIUM', 'red', 3, symbols=['X','X','X'], coin_cost=8),
    Card(1002, 'FORTIFICATIONS', 'red', 3, symbols=['X','X'], resource_cost=['S','S','C','P'], chain_prereq=9),
    Card(1003, 'SIEGE WORKSHOP', 'red', 3, symbols=['X','X'], resource_cost=['W','W','W','G'], chain_prereq=108),
    Card(1004, 'CIRCUS', 'red', 3, symbols=['X','X'], resource_cost=['B','B','S','S'], chain_prereq=109),
    ]
AGE_3_BLUE_CARDS = [
    Card(1005, 'PALACE', 'blue', 3, points=7, resource_cost=['C','S','W','G','G']),
    Card(1006, 'TOWN HALL', 'blue', 3, points=7, resource_cost=['S','S','S','W','W']),
    Card(1007, 'OBELISK', 'blue', 3, points=5, resource_cost=['S','S','G']),
    Card(1008, 'GARDENS', 'blue', 3, points=6, resource_cost=['C','C','W','W'], chain_prereq=111),
    Card(1009, 'PANTHEON', 'blue', 3, points=6, resource_cost=['C','W','P','P'], chain_prereq=112),
    Card(1010, 'SENATE', 'blue', 3, points=5, resource_cost=['C','C','S','P'], chain_prereq=114),
    ]
AGE_3_YELLOW_CARDS = [
    Card(1011, 'LIGHTHOUSE', 'yellow', 3, resource_cost=['C','C','G'], symbols=["*"], symbol_additional_info=['yellow',1], points=3, chain_prereq=15),
    Card(1012, 'ARENA', 'yellow', 3, resource_cost=['C','S','W'], symbols=["*"], symbol_additional_info=['wonder',2], points=3, chain_prereq=118),
    Card(1013, 'CHAMBER OF COMMERCE', 'yellow', 3, resource_cost=['P','P'], symbols=["*"], symbol_additional_info=['gray',3], points=3,),
    Card(1014, 'PORT', 'yellow', 3, resource_cost=['W','G','P'], symbols=["*"], symbol_additional_info=['brown',2], points=3,),
    Card(1015, 'ARMORY', 'yellow', 3, resource_cost=['S','S','G'], symbols=["*"], symbol_additional_info=['red',1], points=3,),
    ]
AGE_3_GREEN_CARDS = [
    Card(1016, 'ACADEMY', 'green', 3, symbols=['>'], points=3, resource_cost=['S','W','G','G']),
    Card(1017, 'STUDY', 'green', 3, symbols=['>'], points=3, resource_cost=['W','W','G','P']),
    Card(1018, 'UNIVERSITY', 'green', 3, symbols=['&'], points=2, resource_cost=['C','G','P'], chain_prereq=121),
    Card(1019, 'OBSERVATORY', 'green', 3, symbols=['&'], points=2, resource_cost=['S','P','P'], chain_prereq=122),
    ]

AGE_3_PURPLE_CARDS = [
    Card(1020, 'MERCHANTS GUILD', 'purple', 3, symbols=['='], resource_cost=['C','W','G','P'], symbol_additional_info=['yellow']),
    Card(1021, 'SHIPOWNERS GUILD', 'purple', 3, symbols=['='], resource_cost=['C','S','G','P'], symbol_additional_info=['brown','gray']),
    Card(1022, 'BUILDERS GUILD', 'purple', 3, symbols=['='], resource_cost=['S','S','C','W','G'], symbol_additional_info=['wonder']),
    Card(1023, 'MAGISTRATES GUILD', 'purple', 3, symbols=['='], resource_cost=['W','W','C','P'], symbol_additional_info=['blue']),
    Card(1024, 'SCIENTISTS GUILD', 'purple', 3, symbols=['='], resource_cost=['C', 'C', 'W','W'], symbol_additional_info=['green']),
    Card(1025, 'MONEYLENDERS GUILD', 'purple', 3, symbols=['='], resource_cost=['S', 'S', 'W','W'], symbol_additional_info=['$']),
    Card(1026, 'TACTICIANS GUILD', 'purple', 3, symbols=['='], resource_cost=['S', 'S', 'C','P'], symbol_additional_info=['red']),
    ]

AGE_3_CARDS =  AGE_3_RED_CARDS + \
               AGE_3_BLUE_CARDS + \
               AGE_3_YELLOW_CARDS + \
               AGE_3_GREEN_CARDS

DECK = [AGE_1_CARDS,AGE_2_CARDS,AGE_3_CARDS]



WONDERS = [
    Card(10000, 'THE COLOSSUS', 'wonder', 0, symbols=['X','X'], points=3, resource_cost=['G','C','C','C']),
    Card(10001, 'THE PYRAMIDS', 'wonder', 0, points=9, resource_cost=['P','S','S','S']),
    Card(10002, 'THE HANGING GARDENS', 'wonder', 0, points=3, symbols=['$',2], resource_cost=['P','G','W','W'], symbol_additional_info=6),
    Card(10003, 'THE TEMPLE OF ARTEMIS', 'wonder', 0, resource_cost=['P','G','S','W'], symbols=['$',2], symbol_additional_info=12),
    Card(10004, 'THE SPHINX', 'wonder', 0, resource_cost=['G','G','C','S'], symbols=[2], points=6),
    Card(10005, 'THE APPIAN WAY', 'wonder', 0, resource_cost=['P','C','C','S','S'], symbols=['$','-',2], points=3, symbol_additional_info=3), #CHANGE THIS?? CUS ITS BOTH 3 LOL
    Card(10006, 'THE GREAT LIGHTHOUSE', 'wonder', 0, resource_cost=['P','P','S','W'], symbols=["+"], symbol_additional_info=['W','S','C'], points=4),
    Card(10007, 'PIRAEUS', 'wonder', 0, resource_cost=['C','S','W','W'], symbols=["+",2], symbol_additional_info=['G','P'],points=2),
    Card(10008, 'THE STATUE OF ZEUS', 'wonder', 0, resource_cost=['P','P','C','W','S'], symbols=['X','kill'], symbol_additional_info=['brown'],points=3),
    Card(10009, 'THE MAUSOLEUM', 'wonder', 0, resource_cost=['P','G','G','C','C'], symbols=['zombie'],points=2),
    Card(10010, 'CIRCUS MAXIMUMS', 'wonder', 0, resource_cost=['G','W','S','S'], symbols=['X','kill'], symbol_additional_info=['gray'],points=3),
    Card(10011, 'THE GREAT LIBRARY', 'wonder', 0, resource_cost=['P','G','W','W','W'], symbols=['science'],points=4),
]



class ScienceToken:
    def __init__(self, token_id, name):
        self.token_id = token_id
        self.name = name

    def __repr__(self):
        return self.name

SCIENCE_TOKENS = [
    ScienceToken(0, 'AGRICULTURE'), #done
    ScienceToken(1, 'ARCHITECTURE'), #done
    ScienceToken(2, 'ECONOMY'), #done
    ScienceToken(3, 'LAW'), #done
    ScienceToken(4, 'MASONRY'), #done
    ScienceToken(5, 'MATHEMATICS'), #done
    ScienceToken(6, 'PHILOSOPHY'), #done
    ScienceToken(7, 'STRATEGY'),  #done - test?
    ScienceToken(8, 'THEOLOGY'), #done
    ScienceToken(9, 'URBANISM'), #done - test?
]