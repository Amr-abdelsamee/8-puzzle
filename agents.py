import numpy as np

class Node:
    def __init__(self, parent, index, state):
        self.state = state
        self.parent = parent
        self.index = index


class Agents:
    def __init__(self, start_state, empty_index, solution):
        self.start_state = start_state
        self.empty_index = empty_index
        self.solution = solution
        self.movable = np.array([[1,3],[0,4,2],[1,5],[0,4,6],[1,3,5,7],[2,4,8],[3,7],[4,6,8],[5,7]])
        self.root = Node(0,0, start_state)
        self.tree = []
        self.tree.append(self.root)

    def next_states(self, current_node):
        new_nodes = []
        for i in self.movable[self.empty_index]:
            state = np.copy(current_node.state)
            state[i], state[self.empty_index] = state[self.empty_index], state[i]
            new_node = Node(current_node.index, len(self.tree), state)
            self.tree.append(new_node)
            new_nodes.append(new_node)
        return new_nodes

    def check_goal(self, state):
        if state == self.solution:
            return True
        return False