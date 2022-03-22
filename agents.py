import numpy as np


class Node:
    def __init__(self, parent, index, state):
        self.state = state
        self.parent = parent
        self.index = index


class Agents:
    def __init__(self, start_state, empty_index, solution):
        self.empty_index = empty_index
        self.solution = solution
        self.movable = np.array(
            [[1, 3], [0, 4, 2], [1, 5], [0, 4, 6], [1, 3, 5, 7], [2, 4, 8], [3, 7], [4, 6, 8], [5, 7]])
        self.root = Node(0, 0, start_state)
        self.current_node = Node(0, 0, start_state)
        self.tree = []
        self.tree.append(self.root)
        self.explored = []
        self.frontier = []

    def next_states(self, current_node):
        new_nodes = []
        for i in self.movable[self.empty_index]:
            state = np.copy(current_node.state)
            state[i], state[self.empty_index] = state[self.empty_index], state[i]
            self.empty_index = i
            for j in self.explored:
                if np.array_equal(state, j):
                    continue
            self.explored.append(state)
            new_node = Node(current_node.index, len(self.tree), state)
            self.tree.append(new_node)
            new_nodes.append(new_node)
        return new_nodes

    def check_goal(self):
        if np.array_equal(self.current_node.state, self.solution):
            return True
        return False


class BFS(Agents):
    def add(self, node):
        self.frontier.append(node)

    def empty(self):
        if len(self.frontier) == 0:
            return False
        return True

    def deq(self):
#
        node = self.frontier[0]
        self.frontier = self.frontier[1:]
        return node

    def update(self):
        new_nodes = self.next_states(self.current_node)
        for i in new_nodes:
            self.add(i)

    def get_path(self):
        node = self.current_node
        path = []
        while node.index != 0:
            path.append(node.state)
            node = self.tree[node.parent]
        return path

    def work(self):
        while not self.check_goal():
            self.update()
            self.current_node = self.deq()
            print(self.current_node.state)

        path = self.get_path()
        path.reverse()
        return path



