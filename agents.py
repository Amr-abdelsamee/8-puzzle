import numpy as np


class Node:
    def __init__(self, parent, index, state):
        self.state = state
        self.parent = parent
        self.index = index


class Agents:
<<<<<<< Updated upstream
    def __init__(self, start_state, empty_index, solution):
        self.empty_index = empty_index
        self.solution = solution
        self.movable = np.array(
            [[1, 3], [0, 4, 2], [1, 5], [0, 4, 6], [1, 3, 5, 7], [2, 4, 8], [3, 7], [4, 6, 8], [5, 7]])
        self.root = Node(0, 0, start_state)
        self.current_node = self.root
        self.tree = []
        self.tree.append(self.root)
        self.explored = []
        self.frontier = []
=======
    def __init__(self, start_state, empty_index, solution, movable):
        self.solution = solution
        self.movable = movable
        self.root = Node(0, 0, start_state, empty_index)
        self.current_node = Node(0, 0, start_state, empty_index)
        self.tree = []
        self.tree.append(self.root)
        self.explored = hashmap(10000)
        self.max_depth = 0

    def contains(self, state):
        return self.explored.search(int(state))
>>>>>>> Stashed changes

    def next_states(self, current_node):
        new_nodes = []
        for i in self.movable[self.empty_index]:
            state = np.copy(current_node.state)
            state[i], state[self.empty_index] = state[self.empty_index], state[i]
            for i in self.explored:
                if state == i:
                    continue
            self.explored.append(state)
            new_node = Node(current_node.index, len(self.tree), state)
            self.tree.append(new_node)
            new_nodes.append(new_node)
        return new_nodes

    def check_goal(self):
        if self.current_node.state == self.solution:
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
        if self.empty():
            return
        else:
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

        path = self.get_path()
        path.reverse()
        return path


class PriorityQueue():
    def __init__(self):
        self.queue = []

    # for checking if the queue is empty
    def isEmpty(self):
        return len(self.queue) == 0

    # for inserting an element in the queue
    def enter(self, node):
        self.queue.append(node)

    # for popping an element based on Priority
    def pop(self):
        try:
            min = 0
            for i in range(len(self.queue)):
                if self.queue[i].cost < self.queue[min].cost:
                    min = i
            item = self.queue[min]
            del self.queue[min]
            return item
        except IndexError:
            print()

def string_to_int(array):
    array = list(array)
    array = ' '.join(array)
    array = np.fromstring(array, dtype=int, sep=' ')
    return array

class AStar(Agents):
    def __init__(self, start_state, empty_index, solution, type):
        super().__init__(start_state, empty_index, solution)
        self.frontier = PriorityQueue()
        self.type = type

    def add(self, node):
        node.cost = self.heu(node.state, self.type) + self.current_node.current_cost
        self.frontier.enter(node)

    def empty(self):
        return self.frontier.isEmpty()

    def deq(self):
        if self.empty():
            raise Exception("kosom da brnamg")
        node = self.frontier.pop()
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
        points = 0
        self.add(self.current_node)
        while not self.check_goal():
            node = self.deq()
            self.current_node = node
            self.update()
            print(self.current_node.state, ' ', points)
            points += 1

        path = self.get_path()
        path.reverse()
        moves = len(path)
        return path, moves, self.max_depth

    def heu(self, state, type):
        """
        calculates heuristics for a given state
        """
        state = string_to_int(state)
        sum = 0
        if type == 1:
            for i in range(3):
                for j in range(3):
                    num = state[i * 3 + j]
                    if num == 0:
                        continue
                    x = (num % 3) - j
                    y = (num // 3) - i
                    sum += abs(x) + abs(y)
        else:
            for i in range(3):
                for j in range(3):
                    num = state[i * 3 + j]
                    if num == 0:
                        continue
                    x = (num % 3) - j
                    y = (num // 3) - i
                    sum += np.sqrt((x ** 2) + (y ** 2))
        return sum