import pygame
from blocks import block

# button class inherite from the block class the check_clicked and draw functions
# buttons are used to create the text box for the game windows
# buttons are used to create the text box to display info  
class Button(block):

    def __init__(self, x_pos, y_pos, width, height, color, label, text_color,font_size):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.color = color
        self.label = label

        self.text_color = text_color
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)
        self.font = pygame.font.SysFont('cambria', font_size)
        self.text = self.font.render(self.label, True, self.text_color)
