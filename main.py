import pygame
from agents import *
from puzzle import Puzzle
from copy import copy
import time


NUM_BLOCKS = 9
SCREEN_WIDTH = 700
SCREEN_HEIGHT = SCREEN_WIDTH
WHITE = (255, 255, 255)

# initializing the pygame
pygame.init()
# create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# title & logo
pygame.display.set_caption("8-puzzle")
# icon = pygame.image.load('\logo.png')
# pygame.display.set_icon(icon)

screen.fill(WHITE)

puzzle = Puzzle(NUM_BLOCKS, screen)

pygame.display.update()

# 125304678
sol1 = '012345678'


labels = ''.join(map(str, puzzle.labels))
hmm = BFS(labels, puzzle.empty_block_index, sol1, puzzle.valid_moves)
start = time.time()
path, moves, depth = hmm.work()
end = time.time()
so_much_time = end - start
print(moves,' ', depth, ' ', so_much_time)
delay = 1

if moves > 30:
    delay = 0.001
puzzle.show_solution(moves, delay, path)
# running loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     x_clicked, y_clicked = pygame.mouse.get_pos()
        #     for i in range(len(blocks)):

        #         if blocks[i].check_clicked(x_clicked, y_clicked):
        #             if not blocks[i].get_label():
        #                 continue
        #             # check_empty_near(i)
        #             check_empty_near(i)
        #             # print(valid_moves)
        pygame.display.update()

pygame.quit()

