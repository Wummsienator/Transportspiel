import pygame
import abc

class GameObject(pygame.sprite.Sprite):
    #initialize object
    def __init__(self, x, y, imageList, screen, font):
        pygame.sprite.Sprite.__init__(self)
        self.imageList = imageList
        self.image_counter = 0
        self.current_image = imageList[self.image_counter]
        self.rect = self.current_image.get_rect()
        self.rect.center = (x, y)
        self.width = self.current_image.get_width()
        self.height = self.current_image.get_height()
        self.screen = screen
        self.font = font

    #get sprite rectangle
    def get_rect(self):
        return self.rect
    
    #get sprite width
    def get_width(self):
        return self.width
    
    #get sprite height
    def get_height(self):
        return self.height
    
    #update method for object parameters
    @abc.abstractmethod
    def update(self):
        print("Not implemented!")

    #draw method for drawing object on screen
    @abc.abstractmethod
    def draw(self, screen):
        print("Not implemented!")
