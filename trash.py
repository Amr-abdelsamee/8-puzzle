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

# background color
screen.fill(WHITE)


# labels = random.sample(range(NUM_BLOCKS), NUM_BLOCKS)


# while not solvable(labels):
    # random.shuffle(labels)

# empty_block_index = get_zero(labels)

# solutions
# solution1 if the empty block is the first one
# solution1 = copy(labels)
# solution1.sort()
# solution1 = list(map(str, solution1))
# solution1[0] = ""
# # solution2 if the empty block is the last one
# solution2 = copy(solution1)
# solution2.pop(0)
# solution2.append("")


puzzle = Puzzle(NUM_BLOCKS, screen)



pygame.display.update()
# 125304678
sol1 = '012345678'


labels = ''.join(map(str, labels))
hmm = BFS(labels, empty_block_index, sol1)
start = time.time()
path, moves, depth = hmm.work()
end = time.time()
so_much_time = end - start
print(moves,' ', depth, ' ', so_much_time)
delay = 1

if moves > 30:
    delay = 0.001

# for move in range(moves):
#     a2 = string_to_int(path[move])
#     replaceable = get_replace(a2)
#     exchange(replaceable)
#     pygame.display.update()
#     time.sleep(delay)

# running loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x_clicked, y_clicked = pygame.mouse.get_pos()
            for i in range(len(blocks)):

                if blocks[i].check_clicked(x_clicked, y_clicked):
                    if not blocks[i].get_label():
                        continue
                    # check_empty_near(i)
                    check_empty_near(i)
                    # print(valid_moves)
        pygame.display.update()

pygame.quit()
