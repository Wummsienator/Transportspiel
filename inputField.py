import pygame

class InputField():
    #initialize object
    def __init__(self, x, y, size_x, size_y, max_length, screen, font, label, initial_text):
        self.rect = pygame.Rect(200, 200, size_x, size_y) 
        self.rect.center = (x, y)
        self.max_length = max_length
        self.screen = screen
        self.font = font
        self.label = label + (": ")
        self.labelSize = self.font.size(self.label)
        self.text = initial_text
        self.color_active = pygame.Color('lightskyblue3') 
        self.color_passive = pygame.Color('antiquewhite2')
        self.color_error = pygame.Color('Red')
        self.active = False
        self.error = False

    #draw method for drawing object on screen
    def draw(self):
        label_text = self.font.render(self.label, 1, pygame.Color("Red"))
        text = self.font.render(self.text, True, pygame.Color('Black'))
        color = self.color_error if self.error else (self.color_active if self.active else self.color_passive)
        pygame.draw.rect(self.screen, color, self.rect)
        self.screen.blit(label_text, (self.rect.x - self.labelSize[0], self.rect.y+5)) 
        self.screen.blit(text, (self.rect.x+5, self.rect.y+5)) 

    #get sprite rectangle
    def get_rect(self):
        return self.rect
    
    #set active status
    def set_active(self, value):
        self.active = value

    #toggle backspace
    def toggle_backspace(self):
        self.text = self.text[:-1]
        self.error = False

    #add symbol to input text
    def add_symbol(self, symbol):
        if (len(self.text) <= self.max_length):
            self.text += symbol
            self.error = False

    #return active status
    def get_active(self):
        return self.active
    
    #return input text
    def get_text(self):
        return self.text
    
    #toggle error status
    def toggle_error(self):
        self.error = True