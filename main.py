import pygame
from blocks import block

def main_menu():
    while True:
        pass

# initializing the pygame
pygame.init()
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
FONT_SIZE = 80
FONT = pygame.font.SysFont('cambria', FONT_SIZE)
RED = (255,0,0)
WHITE = (255, 255, 255)
BLOCK_SIZE = 150
#create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))



#title & logo
pygame.display.set_caption("8-puzzle")
icon = pygame.image.load('D:\programming\python\workspace\8-puzzle\src\logo.png')
pygame.display.set_icon(icon)

#background color
screen.fill(WHITE)

# create rect
x = 65
y = 100
temp = ""
num_filler = 0
space = BLOCK_SIZE + 10
for i in range(0, 3):
    for j in range(0, 3):
        rec = block(x, y, RED, temp, WHITE,FONT, BLOCK_SIZE)
        rec.draw(screen)
        num_filler += 1
        temp = str(num_filler)
        x += space
    x = 65
    y += space


# running loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.update()

pygame.quit()














