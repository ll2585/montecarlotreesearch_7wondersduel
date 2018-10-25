import math


class MonteCarloNode():
    def __init__(self, parent, play, state, unexpanded_plays):
        self.play = play
        self.state = state

        self.n_plays = 0
        self.n_wins = 0

        self.parent = parent
        self.children = {}
        for play in unexpanded_plays:
            self.children[play.hash()] = {'play': play, 'node': None}

    def __repr__(self):
        return str(self.children)

    def child_node(self, play):
        child = self.children[play.hash()]
        if child is None:
            raise Exception("No such play!")
        elif child['node'] is None:
            raise Exception("Child is not expanded!")
        return child['node']

    def expand(self, play, child_state, unexpanded_plays):
        if play.hash() not in self.children:
            raise Exception("No such play!")
        child_node = MonteCarloNode(self, play, child_state, unexpanded_plays)
        self.children[play.hash()] = {'play': play, 'node': child_node}
        return child_node

    def all_plays(self):
        ret = []
        for child in self.children.values():
            ret.append(child['play'])
        return ret

    def unexpanded_plays(self):
        ret = []
        for child in self.children.values():
            if child['node'] is None:
                ret.append(child['play'])
        return ret

    def is_fully_expanded(self):
        for child in self.children.values():
            if child['node'] is None:
                return False
        return True

    def is_leaf(self):
        return len(self.children) == 0

    def get_ucb1(self, bias_param):
        return self.n_wins / self.n_plays + math.sqrt(bias_param * math.log(self.parent.n_plays)/self.n_plays)
