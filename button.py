class Button():
    #initialize object
    def __init__(self, x, y, image, screen):
        self.image = image
        self.rect = image.get_rect()
        self.rect.center = (x, y)
        self.screen = screen

    def get_rect(self):
        return self.rect
    
    #draw method for drawing object on screen
    def draw(self):
        self.screen.blit(self.image, self.rect)