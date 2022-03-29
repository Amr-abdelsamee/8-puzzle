import heapq
import numpy as np
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
        self.state = state 
        self.parent = parent
        self.index = index
        self.empty_index = empty_index
        self.cost = cost
        self.current_cost = current_cost
        self.depth = depth

    def __lt__(self,other):
        return self.cost < other.cost


# Class Agents which all other agents inherit from
class Agents:
    def __init__(self, start_state, empty_index, solution, movable):
        self.solution = solution
        self.movable = movable
        self.root = Node(0, 0, start_state, empty_index)
        self.current_node = Node(0, 0, start_state, empty_index)
        self.tree = []
        self.tree.append(self.root)
        self.explored = set()
        self.max_depth = 0

    # Check if a node with this state is already created
    def contains(self, state):
        return state in self.explored

    # Method to create children of current node
    def next_states(self, current_node):
        new_nodes = [] # Array to hold new nodes
        for i in self.movable[current_node.empty_index]:
            state = list(current_node.state) # List of current state to be swapped
            state[i], state[current_node.empty_index] = state[current_node.empty_index], state[i]
            state = ''.join(state) # Restore state to string
            if  not self.contains(state): # If state is not explored
                self.explored.add(state) # Insert state in explored then create node for it
                new_node = Node(current_node.index, len(self.tree), state, i,
                                current_cost=current_node.current_cost + 1, depth=current_node.depth + 1)
                if new_node.depth > self.max_depth:
                    self.max_depth = new_node.depth
                self.tree.append(new_node) # Add node to parent tree
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
    def deq(self):
        node = self.frontier.pop()
        return node

    # Update method to get children of node
    def update(self):
        new_nodes = self.next_states(self.current_node)
        for i in new_nodes:
            self.add(i)

    # Method to get path by back tracking through the parent tree after reaching goal
    def get_path(self):
        node = self.current_node
        path = []
        while node.index != 0:
            path.append(node.state)
            node = self.tree[node.parent]
        return path

    # Work function to start the search
    def work(self):
        self.add(self.current_node)
        while self.frontier:
            node = self.deq()
            self.current_node = node
            if self.check_goal():
                break
            self.update()
        path = self.get_path()
        path.reverse()
        moves = len(path)
        return path, moves, self.max_depth , len(self.explored)

# BFS Agent
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

    # Method to get path by back tracking through the parent tree after reaching goal
    def get_path(self):
        node = self.current_node
        path = []
        while node.index != 0:
            path.append(node.state)
            node = self.tree[node.parent]
        return path

    # Work function to start the search
    def work(self):

        self.add(self.current_node)
        while self.frontier:
            node = self.deq()
            self.current_node = node
            if self.check_goal():
                break
            self.update()
        path = self.get_path()
        path.reverse()
        moves = len(path)
        return path, moves, self.max_depth , len(self.explored)


# Convert String state to integer array
def string_to_int(array):
    array = list(array)
    array = ' '.join(array)
    array = np.fromstring(array, dtype=int, sep=' ')
    return array


class AStar(Agents):
    # Add frontier to initialization and type of heuristic
    def __init__(self, start_state, empty_index, solution,movable, type):
        super().__init__(start_state, empty_index, solution, movable)
        self.frontier = []
        self.type = type

    # Add to frontier
    def add(self, node):
        node.cost = self.heu(node.state, self.type) + self.current_node.current_cost
        heapq.heappush(self.frontier,node)

    # Pop from frontier
    def deq(self):
        return heapq.heappop(self.frontier)

    # Update method to get children of node
    def update(self):
        new_nodes = self.next_states(self.current_node)
        for i in new_nodes:
            self.add(i)

    # Method to get path by back tracking through the parent tree after reaching goal
    def get_path(self):
        node = self.current_node
        path = []
        while node.index != 0:
            path.append(node.state)
            node = self.tree[node.parent]
        return path

    # Work function to start the search
    def work(self):
        self.add(self.current_node)
        while self.frontier:
            node = self.deq()
            self.current_node = node
            if self.check_goal():
                break
            self.update()
        path = self.get_path()
        path.reverse()
        moves = len(path)
        return path, moves, self.max_depth , len(self.explored)

    # Method calculates heuristics for a given state
    def heu(self, state, type):
        """
        calculates heuristics for a given state
        """
        state = string_to_int(state)
        sum = 0
        if type == 1:               # Manhattan distance
            for i in range(3):
                for j in range(3):
                    num = state[i * 3 + j]
                    if num == 0:
                        continue
                    x = (num % 3) - j
                    y = (num // 3) - i
                    sum += abs(x) + abs(y)
        else:                       # Euclidean distance
            for i in range(3):
                for j in range(3):
                    num = state[i * 3 + j]
                    if num == 0:
                        continue
                    x = (num % 3) - j
                    y = (num // 3) - i
                    sum += np.sqrt((x ** 2) + (y ** 2))
        return sum

    # def decreaseKey(self,parent,cost,index):
    #     state = self.frontier[index]
    #     if state.cost > cost:
    #         state.cost = cost
    #         state.parent = parent