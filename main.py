import math
import pygame
from blocks import block
import math
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
#create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

FONT_SIZE = int(0.5*BLOCK_WIDTH)
FONT = pygame.font.SysFont('cambria', FONT_SIZE)

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
text_filler_str = ""
text_filler_num = 0
# create rect
for i in range(0, NUM_ROW_COL):
    for j in range(0, NUM_ROW_COL):
        rec = block(x, y, BLOCK_COLOR, text_filler_str, text_filler_num, WHITE, FONT, BLOCK_WIDTH, BLOCK_HEIGHT)
        rec.draw(screen)
        blocks.append(rec)
        text_filler_num += 1
        text_filler_str = str(text_filler_num)
        x = x + BLOCK_WIDTH + INBTWN_SPACE
    x = SIDES_PADDING
    y = y + BLOCK_HEIGHT + INBTWN_SPACE


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
                    print(pygame.mouse.get_pos())
                    print(blocks[i].get_position())
        
        pygame.display.update()

pygame.quit()














