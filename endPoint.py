from gameObject import GameObject

class EndPoint(GameObject):
    #initialize object
    def __init__(self, x, y, imageList, screen, font):
        super().__init__(x, y, imageList, screen, font)
        self.amount_ore = 0

    #draw method for drawing object on screen
    def draw(self):
        self.screen.blit(self.current_image, self.rect)

    def deposit_ore(self, amount):
        self.amount_ore += amount 

    def get_amount_ore(self):
        return self.amount_ore