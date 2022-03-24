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
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)
        self.text = FONT.render(self.label, True, self.text_color)
        
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        # screen.blit(self.text, (self.x_pos+int(self.size/2), self.y_pos+int(self.size/2)))
        screen.blit(self.text, (self.x_pos, self.y_pos))
    
    def update(self,screen):
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)
        self.draw(screen)

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

    def get_x_pos(self):
        return self.x_pos
    
    def get_y_pos(self):
        return self.y_pos

    def set_x_pos(self, new_x_pos):
        self.x_pos = new_x_pos
    
    def set_y_pos(self, new_y_pos):
        self.y_pos = new_y_pos
    
    def set_position(self, new_position):
        self.position = new_position
