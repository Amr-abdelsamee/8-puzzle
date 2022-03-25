import numpy as np
import random
from collections import deque


class hashmap:
    def __init__(self, size) -> None:
        self.size = size
        self.hash_table = self.create_table()

    def create_table(self):
        return [[] for _ in range(self.size)]

    def Hashing(self, keyvalue):
        return keyvalue % self.size

    def insert(self, value):
        hash_key = self.Hashing(value)
        self.hash_table[hash_key].append(value)

    def search(self, val):
        hash_key = self.Hashing(val)
        for i in self.hash_table[hash_key]:
            if i == val:
                return True
        return False


class Node:
    def __init__(self, parent, index, state, empty_index, cost=0, current_cost=0, depth=0):
        self.state = state
        self.parent = parent
        self.index = index
        self.empty_index = empty_index
        self.cost = cost
        self.current_cost = current_cost
        self.depth = depth


class Agents:
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

    def next_states(self, current_node):
        new_nodes = []
        random.shuffle(self.movable[current_node.empty_index])
        for i in self.movable[current_node.empty_index]:
            state = list(current_node.state)
            state[i], state[current_node.empty_index] = state[current_node.empty_index], state[i]
            state = ''.join(state)
            if self.contains(state):
                pass
                # print('repeated')
                # print(state)
                # print('...')
            else:
                self.explored.insert(int(state))
                new_node = Node(current_node.index, len(self.tree), state, i,
                                current_cost=current_node.current_cost + 1, depth=current_node.depth + 1)
                if new_node.depth > self.max_depth:
                    self.max_depth = new_node.depth
                self.tree.append(new_node)
                new_nodes.append(new_node)
        return new_nodes

    def check_goal(self):
        if np.array_equal(self.current_node.state, self.solution):
            return True
        return False


class DFS(Agents):
    def __init__(self, start_state, empty_index, solution, movable):
        super().__init__(start_state, empty_index, solution, movable)
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def empty(self):
        print(len(self.frontier))
        if len(self.frontier) == 0:
            return False
        return True

    def deq(self):
        # if self.empty():
        #     raise Exception("kosom da brnamg")
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
        # points = 1
        while not self.check_goal():
            self.update()
            node = self.deq()
            self.current_node = node
            # print(self.current_node.state, ' ', points)
            # points +=1

        path = self.get_path()
        path.reverse()
        moves = len(path)
        return path, moves, self.max_depth, len(self.tree)


class BFS(Agents):

    def __init__(self, start_state, empty_index, solution, movable):
        super().__init__(start_state, empty_index, solution, movable)
        self.frontier = deque()

    def add(self, node):
        self.frontier.append(node)

    def empty(self):
        print(len(self.frontier))
        if len(self.frontier) == 0:
            return False
        return True

    def deq(self):
        # if self.empty():
        #     raise Exception("kosom da brnamg")
        node = self.frontier.popleft()
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
        # points = 0
        self.add(self.current_node)
        while not self.check_goal():
            node = self.deq()
            self.current_node = node
            self.update()
            # print(self.current_node.state, ' ', points)
            # points +=1

        path = self.get_path()
        path.reverse()
        moves = len(path)
        return path, moves, self.max_depth, len(self.tree)


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
    def __init__(self, start_state, empty_index, solution,movable, type):
        super().__init__(start_state, empty_index, solution, movable)
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
        # points = 0
        self.add(self.current_node)
        while not self.check_goal():
            node = self.deq()
            self.current_node = node
            self.update()
            # print(self.current_node.state, ' ', points)
            # points += 1
        path = self.get_path()
        path.reverse()
        moves = len(path)
        return path, moves, self.max_depth, len(self.tree)

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
