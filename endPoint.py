from gameObject import GameObject

class EndPoint(GameObject):
    #initialize object
    def __init__(self, x, y, image_list, screen, font):
        super().__init__(x, y, image_list, screen, font)
        self.amount_ore = 0

    #draw method for drawing object on screen
    def draw(self):
        self.screen.blit(self.current_image, self.rect)

    #receive ore deposit
    def deposit_ore(self, amount):
        self.amount_ore += amount 

    #return currently stored ore amount
    def get_amount_ore(self):
        return self.amount_ore