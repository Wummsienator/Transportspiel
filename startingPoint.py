import pygame
from gameObject import GameObject

class StartingPoint(GameObject):
    #initialize object
    def __init__(self, x, y, imageList, screen, font, amountOre):
        super().__init__(x, y, imageList, screen, font)
        self.amountOre = amountOre
        self.animationCooldown = 15
        self.collect_cooldown = 0

    def set_amount_ore(self, amountOre):
        self.amountOre = amountOre

    #implementation of abstract update method
    def update(self):
        #cooldown for next animation step
        self.animationCooldown -= 1
        if (self.animationCooldown == 0):
            #update image for next animation step
            self.image_counter += 1
            if (self.image_counter > len(self.imageList) - 1):
                self.image_counter = 0
                self.animationCooldown = 100
            else:
                self.animationCooldown = 15
            self.current_image = self.imageList[self.image_counter]

    #implementation of abstract draw method
    def draw(self):
        ore_counter_txt = self.font.render(str(self.amountOre), 1, pygame.Color("RED"))
        text_width = ore_counter_txt.get_width()
        self.screen.blit(self.current_image, self.rect)
        self.screen.blit(ore_counter_txt, (self.rect.x + (self.width / 2) - (text_width / 2), self.rect.y + self.height))  
    
    def collect_ore(self, amount):
        #cooldown for ore collection when truck is standing on starting point
        if (self.collect_cooldown == 0):
            if (amount < self.amountOre):
                self.amountOre -= amount
            else:
                amount = self.amountOre
                self.amountOre = 0
            self.collect_cooldown = 50
            return amount
        else:
            self.collect_cooldown -= 1
            return 0