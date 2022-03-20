import math
import pygame
from blocks import block
import math
import random
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


#initial cordinates of the first block
x = SIDES_PADDING
y = UPPER_PADDING


blocks = []

labels = random.sample(range(NUM_BLOCKS), NUM_BLOCKS)
position = 0
empty_block_index = 0
# create rect
for i in range(0, NUM_ROW_COL):
    for j in range(0, NUM_ROW_COL):
        rec = block(x, y, BLOCK_COLOR, labels[position], position, WHITE, FONT, BLOCK_WIDTH, BLOCK_HEIGHT)
        rec.draw(screen)
        blocks.append(rec)
        # storing the index of the empty block index
        if labels[position]==0: 
            empty_block_index = position 
            print(empty_block_index)
        x = x + BLOCK_WIDTH + INBTWN_SPACE
        position += 1
    x = SIDES_PADDING
    y = y + BLOCK_HEIGHT + INBTWN_SPACE

def exchange(clicked_index):
    global  empty_block_index
    motion_speed = 1
    
    old_x = blocks[clicked_index].get_x_pos()
    new_x = blocks[empty_block_index].get_x_pos()
    old_y = blocks[clicked_index].get_y_pos()
    new_y = blocks[empty_block_index].get_y_pos()

    blocks[clicked_index].set_x_pos(new_x)
    blocks[clicked_index].set_y_pos(new_y)
    blocks[clicked_index].update()
    blocks[clicked_index].draw(screen)

    blocks[empty_block_index].set_x_pos(old_x)
    blocks[empty_block_index].set_y_pos(old_y)
    blocks[empty_block_index].update()
    blocks[empty_block_index].draw(screen)

    temp = blocks[clicked_index]
    blocks[clicked_index] = blocks[empty_block_index]
    blocks[empty_block_index] = temp
    
    empty_block_index = clicked_index


def check_empty_near(clicked_index):
    # check if in upper left corners
    if clicked_index % NUM_ROW_COL == 0 and clicked_index < NUM_ROW_COL:
        if( not blocks[clicked_index + 1].get_label()
        or not blocks[clicked_index + NUM_ROW_COL].get_label()):
            exchange(clicked_index)
    # check if in upper right corners
    elif (clicked_index + 1) % NUM_ROW_COL == 0 and clicked_index < NUM_ROW_COL:
        if( not blocks[clicked_index - 1].get_label()
        or not blocks[clicked_index + NUM_ROW_COL].get_label()):
            exchange(clicked_index)
    # check if in lower left corners
    elif clicked_index % NUM_ROW_COL == 0 and clicked_index >= len(blocks) - NUM_ROW_COL:
        if( not blocks[clicked_index + 1].get_label()
        or not blocks[clicked_index - NUM_ROW_COL].get_label()):
            exchange(clicked_index)
    # check if in lower right corners
    elif (clicked_index + 1) % NUM_ROW_COL == 0 and clicked_index >= len(blocks) - NUM_ROW_COL:
        if( not blocks[clicked_index - 1].get_label()
        or not blocks[clicked_index - NUM_ROW_COL].get_label()):
            exchange(clicked_index)
    # check if the clicked block is in first row
    elif clicked_index < NUM_ROW_COL:
        if( not blocks[clicked_index + 1].get_label()
        or not blocks[clicked_index - 1].get_label()
        or not blocks[clicked_index + NUM_ROW_COL].get_label()):
            exchange(clicked_index)
    # check if the clicked block is in last row
    elif clicked_index >= len(blocks) - NUM_ROW_COL:
        if( not blocks[clicked_index + 1].get_label()
        or not blocks[clicked_index - 1].get_label()
        or not blocks[clicked_index - NUM_ROW_COL].get_label()):
            exchange(clicked_index)
    # check if the clicked block is in first col
    elif clicked_index % NUM_ROW_COL == 0 and clicked_index < NUM_ROW_COL:
        if( not blocks[clicked_index + 1].get_label()
        or not blocks[clicked_index - 1].get_label()
        or not blocks[clicked_index + NUM_ROW_COL].get_label()):
            exchange(clicked_index)
    # check if the clicked block is in last col
    elif clicked_index + 1 % NUM_ROW_COL == 0 and clicked_index < NUM_ROW_COL:
        if( not blocks[clicked_index + 1].get_label()
        or not blocks[clicked_index - 1].get_label()
        or not blocks[clicked_index - NUM_ROW_COL].get_label()):
            exchange(clicked_index)
    # any other place in the middle
    else:
        if( not blocks[clicked_index + 1].get_label()
        or not blocks[clicked_index - 1].get_label()
        or not blocks[clicked_index + NUM_ROW_COL].get_label()
        or not blocks[clicked_index - NUM_ROW_COL].get_label()):
            exchange(clicked_index)


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
                    clicked_index = i
                    check_empty_near(i)
                    print("clicked inedx: "+str(clicked_index))
                    print(pygame.mouse.get_pos())
                    print("get_label: "+str(blocks[i].get_label())+"\n")
        
        pygame.display.update()

pygame.quit()














