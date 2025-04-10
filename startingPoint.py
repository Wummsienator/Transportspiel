import pygame
from gameObject import GameObject

class StartingPoint(GameObject):
    #initialize object
    def __init__(self, x, y, image_list, screen, font, sound, amount_ore):
        super().__init__(x, y, image_list, screen, font)
        self.sound = sound
        self.amount_ore = amount_ore
        self.animationCooldown = 15
        self.collect_cooldown = 0
        self.is_loading = False
        self.sound_playing = False

    #set total amount ore
    def set_amount_ore(self, amount_ore):
        self.amount_ore = amount_ore

    #implementation of abstract update method
    def update(self):
        if (self.animationCooldown == 0):
            #update image for next animation step
            self.image_counter += 1
            if (self.image_counter > len(self.image_list) - 1):
                self.image_counter = 0
                self.animationCooldown = 100
            else:
                self.animationCooldown = 15
            self.current_image = self.image_list[self.image_counter]
        else:
            #cooldown for next animation step
            self.animationCooldown -= 1

        #play sound effect
        if (self.is_loading):
            if not(self.sound_playing):
                self.sound.play(loops=-1, maxtime=0)
                self.sound_playing = True
        else:
            if (self.sound_playing):
                self.sound.stop()
                self.sound_playing = False

    #implementation of abstract draw method
    def draw(self):
        ore_counter_txt = self.font.render(str(self.amount_ore), 1, pygame.Color("WHITE"))
        text_width = ore_counter_txt.get_width()
        self.screen.blit(self.current_image, self.rect)
        self.screen.blit(ore_counter_txt, (self.rect.x + (self.width / 2) - (text_width / 2), self.rect.y + self.height))  
    
    def collect_ore(self, amount):
        #cooldown for ore collection when truck is standing on starting point
        if (self.collect_cooldown == 0):
            if (amount < self.amount_ore):
                self.amount_ore -= amount
            else:
                amount = self.amount_ore
                self.amount_ore = 0
            self.collect_cooldown = 50
            return amount
        else:
            self.collect_cooldown -= 1
            return 0
    
    #set laoding status
    def set_is_loading(self, value):
        self.is_loading = value