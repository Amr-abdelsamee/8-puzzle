import math
import pygame
from copy import copy
import random
import numpy as np
import time
from blocks import block

SCREEN_WIDTH = 600
SCREEN_HEIGHT = SCREEN_WIDTH
SIDES_PADDING = 10
UPPER_PADDING = 100
LOWER_PADDING = 20
INBTWN_SPACE = 1

RED = (255, 0, 0)
vil = (123,44,130)
WHITE = (255, 255, 255)
GREY = (150,150,150)
BLOCK_COLOR = vil
TEXT_COLOR = GREY


class Puzzle:

    def __init__(self, num_blocks, screen):
        self.screen = screen
        self.blocks = []
        self.states = []
        self.labels = []
        self.solution = None
        # self.solution2 = None
        self.empty_block_index = 0
        self.num_blocks = num_blocks
        self.num_row_col = int(math.sqrt(self.num_blocks))
        self.valid_moves = []
        self.states.append(copy(self.blocks))
        self.BLOCK_WIDTH = (SCREEN_WIDTH - (2 * SIDES_PADDING) - (
                    self.num_row_col * INBTWN_SPACE - 1)) / self.num_row_col
        self.BLOCK_HEIGHT = (SCREEN_WIDTH - UPPER_PADDING - LOWER_PADDING - (
                    self.num_row_col * INBTWN_SPACE - 1)) / self.num_row_col
        self.FONT_SIZE = int(0.5 * self.BLOCK_WIDTH)
        self.FONT = pygame.font.SysFont('cambria', self.FONT_SIZE)

        self.create_rects()
        self.valid_moves_generator()
        self.solution_generator()

    def create_rects(self):
        # initial cordinates of the first block
        x = SIDES_PADDING
        y = UPPER_PADDING
        position = 0
        self.labels = random.sample(range(self.num_blocks), self.num_blocks)
        self.labels = [1,0,2,3,4,5,6,7,8]
        while not self.solvable(self.labels):
            random.shuffle(self.labels)

        self.empty_block_index = self.get_zero(self.labels)

        for _ in range(0, self.num_row_col):
            for _ in range(0, self.num_row_col):
                rec = block(x, y, BLOCK_COLOR, self.labels[position], position, TEXT_COLOR, self.FONT, self.BLOCK_WIDTH,
                            self.BLOCK_HEIGHT)
                rec.draw(self.screen)
                self.blocks.append(rec)
                x = x + self.BLOCK_WIDTH + INBTWN_SPACE
                position += 1
            x = SIDES_PADDING
            y = y + self.BLOCK_HEIGHT + INBTWN_SPACE

    def solution_generator(self):
        # solution1 if the empty block is the first one
        self.solution = copy(self.labels)
        self.solution.sort()
        self.solution = list(map(str, self.solution))
        
        self.solution[0] = ""
        # solution2 if the empty block is the last one
        # self.solution2 = copy(self.solution)
        # self.solution2.pop(0)
        # self.solution2.append("")

    def valid_moves_generator(self):
        one_block_moves = []
        for i in range(0, self.num_blocks):
            # one_block_moves = get_neighbors_index(i)
            one_block_moves = self.get_neighbors_index(i)
            self.valid_moves.append(one_block_moves)
        print(self.valid_moves)

    def get_neighbors_index(self, index):
        neighbors_indexs = []
        # check if in upper left corners
        if index == 0:
            neighbors_indexs.append(index + 1)
            neighbors_indexs.append(index + self.num_row_col)

        # check if in upper right corners
        elif index == (self.num_row_col - 1):
            neighbors_indexs.append(index - 1)
            neighbors_indexs.append(index + self.num_row_col)

        # check if in lower left corners
        elif index == (self.num_row_col ** 2 - self.num_row_col):
            neighbors_indexs.append(index - self.num_row_col)
            neighbors_indexs.append(index + 1)

        # check if in lower right corners
        elif index == (self.num_row_col ** 2 - 1):
            neighbors_indexs.append(index - self.num_row_col)
            neighbors_indexs.append(index - 1)

        # check if the in first cols
        elif index % self.num_row_col == 0:
            neighbors_indexs.append(index - self.num_row_col)
            neighbors_indexs.append(index + 1)
            neighbors_indexs.append(index + self.num_row_col)

        # check if in last col
        elif (index + 1) % self.num_row_col == 0:
            neighbors_indexs.append(index - self.num_row_col)
            neighbors_indexs.append(index - 1)
            neighbors_indexs.append(index + self.num_row_col)

        # check if in first row
        elif index < self.num_row_col:
            neighbors_indexs.append(index - 1)
            neighbors_indexs.append(index + 1)
            neighbors_indexs.append(index + self.num_row_col)
    
        # check if in last row
        elif index >= len(self.blocks) - self.num_row_col:
            neighbors_indexs.append(index - 1)
            neighbors_indexs.append(index + 1)
            neighbors_indexs.append(index - self.num_row_col)

        # any other place in the middle
        else:
            neighbors_indexs.append(index - self.num_row_col)
            neighbors_indexs.append(index - 1)
            neighbors_indexs.append(index + 1)
            neighbors_indexs.append(index + self.num_row_col)
        return (copy(neighbors_indexs))

    def check_empty_near(self, clicked_index):
        if self.empty_block_index in self.valid_moves[clicked_index]:
            self.exchange(clicked_index)

    def exchange(self, clicked_index):
        empty_block_index = self.empty_block_index

        old_x = self.blocks[clicked_index].get_x_pos()
        new_x = self.blocks[empty_block_index].get_x_pos()
        old_y = self.blocks[clicked_index].get_y_pos()
        new_y = self.blocks[empty_block_index].get_y_pos()

        self.blocks[clicked_index].set_x_pos(new_x)
        self.blocks[clicked_index].set_y_pos(new_y)
        self.blocks[clicked_index].update(self.screen)

        self.blocks[empty_block_index].set_x_pos(old_x)
        self.blocks[empty_block_index].set_y_pos(old_y)
        self.blocks[empty_block_index].update(self.screen)

        temp = self.blocks[clicked_index]
        self.blocks[clicked_index] = self.blocks[empty_block_index]
        self.blocks[empty_block_index] = temp

        # update the states
        self.states.append(copy(self.blocks))
        # set the new index of the empty block
        self.empty_block_index = clicked_index

    def check_solved(self):
        solved = True
        for i in range(1,len(self.blocks)):
            # print(str(blocks[i].get_label())+"_comp1_"+str(solution1[i]))
            if self.blocks[i].get_label() != self.solution[i]:
                solved = False
        # if solved: return solved
        # solved = True
        # for i in range(len(self.blocks)):
        #     # print(str(blocks[i].get_label())+"_comp2_"+str(solution2[i]))
        #     if self.blocks[i].get_label() != self.solution2[i]:
        #         solved = False
        return solved

    def show_steps(self):
        print("moves record:")
        for i in range(len(self.states)):
            for j in range(len(self.blocks)):
                print(self.states[i][j].get_label(), end=" ")
            print()

    def getInvCount(self, arr):
        inversions = 0
        empty_value = 0
        for i in range(0, 9):
            for j in range(i + 1, 9):
                if arr[j] != empty_value and arr[i] != empty_value and arr[i] > arr[j]:
                    inversions += 1
        return inversions

    def solvable(self, array):
        inversions = self.getInvCount(array)
        return inversions % 2 == 0

    def get_zero(self, array):
        for i in range(len(array)):
            if array[i] == 0:
                return i
        return -1

    def show_solution(self, moves, delay, path):
        for move in range(moves):
            a2 = self.string_to_int(path[move])
            replaceable = self.get_zero(a2)
            self.exchange(replaceable)
            pygame.display.update()
            time.sleep(delay)

    def string_to_int(self, array):
        array = list(array)
        array = ' '.join(array)
        array = np.fromstring(array, dtype=int, sep=' ')
        return array
