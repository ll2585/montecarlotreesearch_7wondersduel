import datetime
from monte_carlo_node import MonteCarloNode
import copy
import math
import random

from is_monte_carlo_node import Node

class MonteCarlo():
    def __init__(self, game, ucb1_explore_param = 2):
        self.game = game
        self.ucb1_explore_param = ucb1_explore_param
        self.nodes = {}

    def get_move(self):
        root_state = self.game.get_state()
        current_player_id = root_state.current_player_id
        rootnode = Node()
        print("----")
        #for i in range(1000):
        timeout = 1
        end = datetime.datetime.now() + datetime.timedelta(milliseconds=timeout * 1000)

        while datetime.datetime.now() < end:
            node = rootnode
            state = root_state.clone_and_randomize(current_player_id)

            simulated_game = self.game.new_game_from_state(state)
            #print(simulated_game.get_possible_moves())
            while simulated_game.get_possible_moves() != [] and node.GetUntriedMoves(simulated_game.get_possible_moves()) == []:
                node = node.UCBSelectChild(simulated_game.get_possible_moves())
                simulated_game.do_move(node.move)

            #expand
            untried_moves = node.GetUntriedMoves(simulated_game.get_possible_moves())
            #print(untried_moves)
            if untried_moves != []:  # if we can expand (i.e. state/node is non-terminal)
                m = random.choice(untried_moves)
                player = simulated_game.get_current_player_id()
                simulated_game.do_move(m)
                node = node.AddChild(m, player)  # add child and descend tree

            # Simulate
            while simulated_game.get_possible_moves() != []:  # while state is non-terminal
                simulated_game.do_move(random.choice(simulated_game.get_possible_moves()))

            while node != None:  # backpropagate from the expanded node and work back to the root node
                node.Update(simulated_game)
                node = node.parentNode

        print(rootnode.ChildrenToString())

        return max(rootnode.childNodes, key=lambda c: c.visits).move  # return the move that was most visited

    def make_node(self, state):
        if not state.hash() in self.nodes:
            unexpanded_plays = copy.copy(self.game.legal_plays(state)) #TODO: deep copy?
            node = MonteCarloNode(None, None, state, unexpanded_plays)
            self.nodes[state.hash()] = node

    def run_search(self, state, timeout = 3):
        self.make_node(state)

        draws = 0
        total_sims = 0
        end = datetime.datetime.now() + datetime.timedelta(milliseconds=timeout * 1000)

        while datetime.datetime.now() < end:
            simulated_state = state.clone_and_randomize()
            self.make_node(simulated_state)
            node = self.select(simulated_state)
            winner = self.game.winner(node.state)

            if not node.is_leaf() and winner is None:
                node = self.expand(node)
                winner = self.simulate(node)

            self.backpropagate(node, winner)

            if winner == 0:
                draws += 1
            total_sims += 1

        return {'runtime': timeout, 'simulations': total_sims, 'draws': draws}

    def best_play(self, state, policy = 'robust'):
        self.make_node(state)
        if not self.nodes[state.hash()].is_fully_expanded():
            raise Exception("Not enough information!")

        node = self.nodes[state.hash()]
        all_plays = node.all_plays()
        best_play = None

        if policy == 'robust':
            max = float('-inf')
            for play in all_plays:
                child_node = node.child_node(play)
                if child_node.n_plays > max:
                    best_play = play
                    max = child_node.n_plays
        elif policy == 'max':
            max = float('-inf')
            for play in all_plays:
                child_node = node.child_node(play)
                ratio = child_node.n_wins / child_node.n_plays
                if ratio > max:
                    best_play = play
                    max = ratio
        return best_play



    def select(self, state):
        node = self.nodes[state.hash()]
        while node.is_fully_expanded() and not node.is_leaf():
            plays = node.all_plays()
            best_play = None
            best_ucb1 = float('-inf')
            for play in plays:
                child_ucb1 = node.child_node(play).get_ucb1(self.ucb1_explore_param)
                if child_ucb1 > best_ucb1:
                    best_play = play
                    best_ucb1 = child_ucb1
            node = node.child_node(best_play)
        return node


    def expand(self, node):
        plays = node.unexpanded_plays()
        index = math.floor(random.random() * len(plays)) #TODO: improve
        play = plays[index]
        child_state = self.game.next_state(node.state, play)
        child_unexpanded_plays = self.game.legal_plays(child_state)
        child_node = node.expand(play, child_state, child_unexpanded_plays)
        self.nodes[child_state.hash()] = child_node
        return child_node

    def simulate(self, node):
        state = node.state
        winner = self.game.winner(state)
        while winner is None:
            plays = self.game.legal_plays(state)
            play = plays[math.floor(random.random() * len(plays))]  #TODO: better way to do this
            state = self.game.next_state(state, play)
            winner = self.game.winner(state)
        return winner

    def backpropagate(self, node, winner):
        while node is not None:
            node.n_plays += 1
            if node.state.is_player(-winner):
                node.n_wins += 1
            node = node.parent

    def get_stats(self, state):
        node = self.nodes[state.hash()]
        stats = {'n_plays': node.n_plays, 'n_wins': node.n_wins, 'children': []}
        for child in node.children.values():
            if child['node'] is None:
                stats['children'].append({'play': child['play'], 'n_plays': None, 'n_wins': None})
            else:
                stats['children'].append({'play': child['play'], 'n_plays': child['node'].n_plays, 'n_wins': child['node'].n_wins, 'percentage': '{0:.1f}'.format(child['node'].n_wins/child['node'].n_plays*100)})
        return stats
