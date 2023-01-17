import math
import copy
import random
import time
from Poddavki import Poddavki


def getTurn(game: Poddavki):
    mcts = MonteCarlo(game)
    mcts.search(1)
    return mcts.best_move()


# https://www.harrycodes.com/blog/monte-carlo-tree-search
class Node:
    def __init__(self, move, parent, explore=math.sqrt(2)):
        self.move = move
        self.parent = parent
        self.N = 0
        self.Q = 0
        self.explore = explore
        self.children = {}

    def add_children(self, children):
        for child in children:
            self.children[child.move] = child

    def value(self):
        if self.N == 0:
            return 0 if self.explore == 0 else math.inf
        else:
            return self.Q / self.N + self.explore * math.sqrt(math.log(self.parent.N) / self.N)


class MonteCarlo:
    def __init__(self, state=Poddavki()):
        self.root_state = copy.deepcopy(state)
        self.root = Node(None, None)
        self.run_time = 0
        self.node_count = 0
        self.num_rollouts = 0

    def select_node(self):
        node = self.root
        state = copy.deepcopy(self.root_state)

        while len(node.children) != 0:
            children = node.children.values()
            max_value = max(children, key=lambda n: n.value()).value()
            max_nodes = [n for n in children if n.value() == max_value]

            node = random.choice(max_nodes)
            state.applyMove(node.move)

            if node.N == 0:
                return node, state

        if self.expand(node, state):
            node = random.choice(list(node.children.values()))
            state.applyMove(node.move)

        return node, state

    def expand(self, parent, state):
        if not state.hasAvailableMoves():
            return False

        children = [Node(move, parent) for move in state.getPossibleMoves(state.to_move)]
        parent.add_children(children)

        return True

    def roll_out(self, state):
        while state.hasAvailableMoves():
            state.applyMove(random.choice(state.getPossibleMoves(state.to_move)))

        return state.get_outcome()

    def back_propagate(self, node, turn, outcome):

        # For the current player, not the next player
        reward = 0 if outcome == turn else 1

        while node is not None:
            node.N += 1
            node.Q += reward
            node = node.parent
            if outcome == 'draw':
                reward = 0
            else:
                reward = 1 - reward

    def search(self, time_limit):
        start_time = time.process_time()

        num_rollouts = 0
        while time.process_time() - start_time < time_limit:
            node, state = self.select_node()
            outcome = self.roll_out(state)
            self.back_propagate(node, state.to_move, outcome)
            num_rollouts += 1

        run_time = time.process_time() - start_time
        self.run_time = run_time
        self.num_rollouts = num_rollouts

    def best_move(self):
        max_value = max(self.root.children.values(), key=lambda n: n.N).N
        max_nodes = [n for n in self.root.children.values() if n.N == max_value]
        best_child = random.choice(max_nodes)

        return best_child.move

    def mc_move(self, move):
        if move in self.root.children:
            self.root_state.applyMove(move)
            # self.root_state.move(move)
            self.root = self.root.children[move]
            return

        # self.root_state.move(move)
        self.root_state.applyMove(move)
        self.root = Node(None, None)

    def statistics(self):
        return self.num_rollouts, self.run_time
