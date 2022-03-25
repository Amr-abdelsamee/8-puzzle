import numpy as np
import random
from collections import deque


# Creating hash map class to add explored nodes in it
class Hashmap:
    # initialize with size and create table
    def __init__(self, size) -> None:
        self.size = size
        self.hash_table = self.create_table()

    # Create empty table
    def create_table(self):
        return [[] for _ in range(self.size)]

    # Function to get key
    def hashing(self, keyvalue):
        return keyvalue % self.size

    # Insert to hash table
    def insert(self, value):
        hash_key = self.hashing(value)
        self.hash_table[hash_key].append(value)

    # Find if element is in hash table
    def search(self, val):
        hash_key = self.hashing(val)
        for i in self.hash_table[hash_key]:
            if i == val:
                return True
        return False


# Class Node with all required node data to form a tree
class Node:
    def __init__(self, parent, index, state, empty_index, cost=0, current_cost=0, depth=0):
        self.state = state  # State in string form
        self.parent = parent  # Parent index in tree array
        self.index = index  # Node index in tree
        self.empty_index = empty_index  # The zero index in the state
        self.cost = cost  # Cost to be used by A*
        self.current_cost = current_cost  # Actual cost to reach this node (Depth)


# Class Agents which all other agents inherit from
class Agents:
    def __init__(self, start_state, empty_index, solution, movable):
        self.solution = solution  # Solution is set to be changeable
        self.movable = movable  # Movable array of arrays for each index of zero
        self.root = Node(0, 0, start_state, empty_index)  # Initial state node
        self.current_node = Node(0, 0, start_state, empty_index)  # First node to be used
        self.tree = []  # Empty tree array
        self.tree.append(self.root)  # Append the root to tree
        self.explored = Hashmap(10000)  # Creating explored as hashmap object
        self.max_depth = 0  # Depth of deepest leaf

    # Check if a node with this state is already created
    def contains(self, state):
        return self.explored.search(int(state))

    # Method to create children of current node
    def next_states(self, current_node):
        new_nodes = []  # Array to hold new nodes
        random.shuffle(self.movable[current_node.empty_index])  # Randomize which index chooses to replace with first
        for i in self.movable[current_node.empty_index]:
            state = list(current_node.state)  # List of current state to be swapped
            state[i], state[current_node.empty_index] = state[current_node.empty_index], state[i]
            state = ''.join(state)  # Restore state to string
            if self.contains(state):
                pass  # If state is existing do nothing
            else:
                self.explored.insert(int(state))  # Insert state in explored then create node ti
                new_node = Node(current_node.index, len(self.tree), state, i,
                                current_cost=current_node.current_cost + 1)
                if new_node.current_cost > self.max_depth:
                    self.max_depth = new_node.current_cost
                self.tree.append(new_node)  # Add node to tree
                new_nodes.append(new_node)
        return new_nodes

    # Function to check if goal reached
    def check_goal(self):
        if np.array_equal(self.current_node.state, self.solution):
            return True
        return False


# DFS Agent
class DFS(Agents):
    # Add frontier to initialization
    def __init__(self, start_state, empty_index, solution, movable):
        super().__init__(start_state, empty_index, solution, movable)
        self.frontier = []

    # Add to frontier
    def add(self, node):
        self.frontier.append(node)

    # Pop from frontier
    def pop(self):
        node = self.frontier.pop()
        return node

    # Update method to get children of node
    def update(self):
        new_nodes = self.next_states(self.current_node)
        for i in new_nodes:
            self.add(i)

    # Method to get path by back tracking after reaching goal
    def get_path(self):
        node = self.current_node
        path = []
        while node.index != 0:
            path.append(node.state)
            node = self.tree[node.parent]
        return path

    # Work function to run the agent
    def work(self):
        while not self.check_goal():
            self.update()
            node = self.pop()
            self.current_node = node

        path = self.get_path()
        path.reverse()
        moves = len(path)
        return path, moves, self.max_depth, len(self.tree)


class BFS(Agents):
    # Add frontier to initialization
    def __init__(self, start_state, empty_index, solution, movable):
        super().__init__(start_state, empty_index, solution, movable)
        self.frontier = deque()

    # Add to frontier
    def add(self, node):
        self.frontier.append(node)

    # Deque from frontier
    def deq(self):
        node = self.frontier.popleft()
        return node

    # Update method to get children of node
    def update(self):
        new_nodes = self.next_states(self.current_node)
        for i in new_nodes:
            self.add(i)

    # Method to get path by back tracking after reaching goal
    def get_path(self):
        node = self.current_node
        path = []
        while node.index != 0:
            path.append(node.state)
            node = self.tree[node.parent]
        return path

    # Work function to run the agent
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


# Priority Queue class to be used by A* agent
class PriorityQueue:
    def __init__(self):
        self.queue = []

    # for checking if the queue is empty
    def isEmpty(self):
        return len(self.queue) == 0

    # for inserting an element in the queue
    def enter(self, node):
        self.queue.append(node)

    # for popping an element based on Priority (Lowest Cost)
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


# Convert String state to integer array
def string_to_int(array):
    array = list(array)
    array = ' '.join(array)
    array = np.fromstring(array, dtype=int, sep=' ')
    return array


class AStar(Agents):
    # Add frontier to initialization and type of heuristic
    def __init__(self, start_state, empty_index, solution, movable, type):
        super().__init__(start_state, empty_index, solution, movable)
        self.frontier = PriorityQueue()
        self.type = type

    # Add to frontier
    def add(self, node):
        node.cost = self.heu(node.state, self.type) + self.current_node.current_cost
        self.frontier.enter(node)

    # Pop from frontier
    def pop(self):
        node = self.frontier.pop()
        return node

    # Update method to get children of node
    def update(self):
        new_nodes = self.next_states(self.current_node)
        for i in new_nodes:
            self.add(i)

    # Method to get path by back tracking after reaching goal
    def get_path(self):
        node = self.current_node
        path = []
        while node.index != 0:
            path.append(node.state)
            node = self.tree[node.parent]
        return path

    # Work function to run the agent
    def work(self):
        # points = 0
        self.add(self.current_node)
        while not self.check_goal():
            node = self.pop()
            self.current_node = node
            self.update()
            # print(self.current_node.state, ' ', points)
            # points += 1
        path = self.get_path()
        path.reverse()
        moves = len(path)
        return path, moves, self.max_depth, len(self.tree)

    # Method calculates heuristics for a given state
    def heu(self, state, type):
        state = string_to_int(state)
        sum = 0
        if type == 1:           # Manhattan distance
            for i in range(3):
                for j in range(3):
                    num = state[i * 3 + j]
                    if num == 0:
                        continue
                    x = (num % 3) - j
                    y = (num // 3) - i
                    sum += abs(x) + abs(y)
        else:               # Euclidean distance
            for i in range(3):
                for j in range(3):
                    num = state[i * 3 + j]
                    if num == 0:
                        continue
                    x = (num % 3) - j
                    y = (num // 3) - i
                    sum += np.sqrt((x ** 2) + (y ** 2))
        return sum
