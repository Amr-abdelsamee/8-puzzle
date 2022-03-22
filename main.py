import math
import pygame
from blocks import block
import math
import random
from copy import copy
def main_menu():
    while True:
        pass

# initializing the pygame
pygame.init()
SCREEN_WIDTH = 600
SCREEN_HEIGHT = SCREEN_WIDTH

RED = (255,0,0)
WHITE = (255, 255, 255)

SIDES_PADDING = 10
UPPER_PADDING = 100
LOWER_PADDING = 20
INBTWN_SPACE = 1
NUM_BLOCKS = 9
NUM_ROW_COL = int(math.sqrt(NUM_BLOCKS))
BLOCK_WIDTH = (SCREEN_WIDTH - (2*SIDES_PADDING) - (NUM_ROW_COL*INBTWN_SPACE-1)) / NUM_ROW_COL
BLOCK_HEIGHT = (SCREEN_WIDTH - UPPER_PADDING - LOWER_PADDING - (NUM_ROW_COL*INBTWN_SPACE-1)) / NUM_ROW_COL
BLOCK_COLOR = RED
FONT_SIZE = int(0.5*BLOCK_WIDTH)
FONT = pygame.font.SysFont('cambria', FONT_SIZE)

#create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


#title & logo
pygame.display.set_caption("8-puzzle")
icon = pygame.image.load('D:\programming\python\workspace\8-puzzle\src\logo.png')
pygame.display.set_icon(icon)

#background color
screen.fill(WHITE)


# array to store the blocks
blocks = []
# array to store the steps taken while solving the puzzle
states = []

#initial values
labels = []
empty_block_index = 0
valid_moves = []

def create_rects():
    #initial cordinates of the first block
    x = SIDES_PADDING
    y = UPPER_PADDING
    global labels
    labels = random.sample(range(NUM_BLOCKS), NUM_BLOCKS)
    position = 0
    global empty_block_index
    for i in range(0, NUM_ROW_COL):
        for j in range(0, NUM_ROW_COL):
            rec = block(x, y, BLOCK_COLOR, labels[position], position, WHITE, FONT, BLOCK_WIDTH, BLOCK_HEIGHT)
            rec.draw(screen)
            blocks.append(rec)
            # storing the index of the empty block index
            if labels[position]==0: 
                empty_block_index = position 
            x = x + BLOCK_WIDTH + INBTWN_SPACE
            position += 1
        x = SIDES_PADDING
        y = y + BLOCK_HEIGHT + INBTWN_SPACE

def valid_moves_generator():
    one_block_moves = []
    for i in range(0, NUM_BLOCKS):
        # one_block_moves = get_neighbors_index(i)
        one_block_moves = get_neighbors_index(i)
        valid_moves.append(one_block_moves)

def get_neighbors_index(index):
    neighbors_indexs = []
    # check if in upper left corners
    if index == 0:
        neighbors_indexs.append(index + 1)
        neighbors_indexs.append(index + NUM_ROW_COL)

    # check if in upper right corners
    elif index == (NUM_ROW_COL-1):
        neighbors_indexs.append(index - 1)
        neighbors_indexs.append(index + NUM_ROW_COL)

    # check if in lower left corners
    elif index == (NUM_ROW_COL**2 - NUM_ROW_COL):
        neighbors_indexs.append(index - NUM_ROW_COL)
        neighbors_indexs.append(index + 1)

    # check if in lower right corners
    elif index == (NUM_ROW_COL**2 - 1):
        neighbors_indexs.append(index - NUM_ROW_COL)
        neighbors_indexs.append(index - 1)

    # check if in first row
    elif index < NUM_ROW_COL:
        neighbors_indexs.append(index - 1)
        neighbors_indexs.append(index + 1)
        neighbors_indexs.append(index + NUM_ROW_COL)

    # check if in last row
    elif index >= len(blocks) - NUM_ROW_COL:
        neighbors_indexs.append(index - 1)
        neighbors_indexs.append(index + 1)
        neighbors_indexs.append(index - NUM_ROW_COL)

    # check if the in first cols
    elif index % NUM_ROW_COL == 0:
        neighbors_indexs.append(index - NUM_ROW_COL)
        neighbors_indexs.append(index + 1)
        neighbors_indexs.append(index + NUM_ROW_COL)
    
    # check if in last col
    elif (index + 1) % NUM_ROW_COL == 0:
        neighbors_indexs.append(index - NUM_ROW_COL)
        neighbors_indexs.append(index - 1)
        neighbors_indexs.append(index + NUM_ROW_COL)

    # any other place in the middle
    else:
        neighbors_indexs.append(index - NUM_ROW_COL)
        neighbors_indexs.append(index - 1)
        neighbors_indexs.append(index + 1)
        neighbors_indexs.append(index + NUM_ROW_COL)
    return(copy(neighbors_indexs))

def check_empty_near(clicked_index):
    if empty_block_index in valid_moves[clicked_index]:
        exchange(clicked_index)

def exchange(clicked_index):

    global  empty_block_index
    
    old_x = blocks[clicked_index].get_x_pos()
    new_x = blocks[empty_block_index].get_x_pos()
    old_y = blocks[clicked_index].get_y_pos()
    new_y = blocks[empty_block_index].get_y_pos()

    blocks[clicked_index].set_x_pos(new_x)
    blocks[clicked_index].set_y_pos(new_y)
    blocks[clicked_index].update(screen)

    blocks[empty_block_index].set_x_pos(old_x)
    blocks[empty_block_index].set_y_pos(old_y)
    blocks[empty_block_index].update(screen)

    temp = blocks[clicked_index]
    blocks[clicked_index] = blocks[empty_block_index]
    blocks[empty_block_index] = temp

    #update the states
    states.append(copy(blocks))
    #set the new index of the empty block
    empty_block_index = clicked_index

    print_info()

def check_solved():
    solved = True
    for i in range(len(blocks)):
        # print(str(blocks[i].get_label())+"_comp1_"+str(solution1[i]))
        if blocks[i].get_label() != solution1[i]:
            solved = False
    if solved: return solved
    solved = True
    for i in range(len(blocks)):
        # print(str(blocks[i].get_label())+"_comp2_"+str(solution2[i]))
        if blocks[i].get_label() != solution2[i]:
            solved = False
    return solved

def show_steps():
    print("moves record:")
    for i in range(len(states)):
        for j in range(len(blocks)):
            print(states[i][j].get_label(), end =" ")
        print()

def print_info():
    show_steps()
    print("solved: " + str(check_solved()))


create_rects()
valid_moves_generator()
#initial state is added
states.append(copy(blocks))

#solutions
# solution1 if the empty block is the first one
solution1 = copy(labels) 
solution1.sort()
solution1 = list(map(str, solution1))
solution1[0] = ""
# solution2 if the empty block is the last one
solution2 = copy(solution1) 
solution2.pop(0)
solution2.append("")


# running loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x_clicked,y_clicked = pygame.mouse.get_pos()
            for i in range(len(blocks)):
                
                if blocks[i].check_clicked(x_clicked, y_clicked):
                    if not blocks[i].get_label():
                        continue
                    # check_empty_near(i)
                    check_empty_near(i)
                    # print(valid_moves)
        pygame.display.update()

pygame.quit()














