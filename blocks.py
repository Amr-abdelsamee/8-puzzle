import pygame

class block:
    def __init__(self, x_pos, y_pos, color, label, position, text_color, FONT, width, height):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.color = color
        if label == 0:self.label = ""
        else:self.label = str(label)
        self.position = position
        self.text_color = text_color
        
        self.text = FONT.render(self.label, True, self.text_color)
        self.width = width
        self.height = height
        
    def draw(self,screen):
        pygame.draw.rect(screen,self.color, (self.x_pos, self.y_pos, self.width, self.height))

        # screen.blit(self.text, (self.x_pos+int(self.size/2), self.y_pos+int(self.size/2)))
        screen.blit(self.text, (self.x_pos, self.y_pos))
        
    def check_clicked(self, x_clicked , y_clicked):
        if( x_clicked >= self.x_pos 
        and x_clicked < self.x_pos + self.width
        and y_clicked >= self.y_pos
        and y_clicked < self.y_pos + self.height):
            return True
        
    def get_label(self):
        return self.label
    
    def get_position(self):
        return self.position
