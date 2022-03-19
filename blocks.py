import pygame

class block:
    def __init__(self, x_pos, y_pos, color, text, text_color, FONT, width, height):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.color = color
        self.text_color = text_color
        self.text_in = text
        self.text = FONT.render(self.text_in, True, self.text_color)
        self.width = width
        self.height = height
        
    def draw(self,screen):
        pygame.draw.rect(screen,self.color, (self.x_pos, self.y_pos, self.width, self.height))

        # screen.blit(self.text, (self.x_pos+int(self.size/2), self.y_pos+int(self.size/2)))
        screen.blit(self.text, (self.x_pos, self.y_pos))
        