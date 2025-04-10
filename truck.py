import pygame
from gameObject import GameObject

class Truck(GameObject):
    #initialize object
    def __init__(self, x, y, imageList, screen, font, sound, speed, capacity, maxFuel, consumption):
        super().__init__(x, y, imageList, screen, font)
        self.sound = sound
        self.alive = True
        self.speed = speed
        self.currentOre = 0
        self.capacity = capacity
        self.currentFuel = maxFuel
        self.maxFuel = maxFuel
        self.consumption = consumption
        self.consumption_countdown = 10
        self.refuel_cooldown = 20
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        self.is_collecting = False
        self.is_refueling = False
        self.sound_playing = False

    #return alive status
    def get_alive(self):
        return self.alive
    
    #check alive status
    def check_alive(self):
        if (self.currentFuel <= 0):
            self.currentFuel = 0
            self.alive = False

    #implementation of abstract update method
    def update(self):
        if self.get_alive():
            dx = 0
            dy = 0

            #update image and rectangle on moving direction
            old_center = self.rect.center
            if self.moving_left:
                dx -= self.speed
                self.current_image = self.imageList[self.image_counter]
            elif self.moving_right:
                dx += self.speed
                self.current_image = pygame.transform.flip(self.imageList[self.image_counter], True, False)
            elif self.moving_up:
                dy -= self.speed
                self.current_image = pygame.transform.rotate(self.imageList[self.image_counter], 270)
            elif self.moving_down:
                dy += self.speed
                self.current_image = pygame.transform.rotate(self.imageList[self.image_counter], 90)

            self.rect = self.current_image.get_rect()
            self.rect.center = old_center
            self.width = self.current_image.get_width()
            self.height = self.current_image.get_height()

            #check collision with screen ends
            w,h = self.screen.get_size()
            if (self.rect.x + dx < 0 or self.rect.x + self.width + dx > w):
                dx = 0
            if (self.rect.y + dy < 0 or self.rect.y + self.height + dy > h): 
                dy = 0      

            #update rectangle position after moving
            self.rect.x += dx
            self.rect.y += dy

            if (dx != 0 or dy != 0):
                if not(self.sound_playing):
                    self.sound.play(loops=-1, maxtime=0) # Loops indefinitely
                    self.sound_playing = True
            else:
                if (self.sound_playing):
                    self.sound.stop()
                    self.sound_playing = False

            #consume fuel
            if (self.consumption_countdown == 0):
                if not(self.is_refueling):
                    self.currentFuel -= self.consumption
                    self.consumption_countdown = 10
            else:
                self.consumption_countdown -= 1

            #refuel
            if (self.refuel_cooldown == 0):
                if (self.is_refueling):
                    self.refuel()
                    self.refuel_cooldown = 20
            else:
                self.refuel_cooldown -= 1

            self.check_alive()

    #implementation of abstract draw method
    def draw(self):
        self.screen.blit(self.current_image, self.rect)

    #stop all actions
    def kill(self):
        self.alive = False
        self.sound.stop()
        self.sound_playing = False

    #set max capacity
    def set_capacity(self, capacity):
        self.capacity = capacity

    #return max capacity
    def get_capacity(self):
        return self.capacity
    
    #set consumption
    def set_consumption(self, consumption):
        self.consumption = consumption

    #set speed
    def set_speed(self, speed):
        self.speed = speed

    #collect ore
    def collect_ore(self, amount):
        self.currentOre += amount

    #reset current ore
    def reset_ore(self):
        temp = self.currentOre 
        self.currentOre = 0
        return temp

    #return current ore
    def get_current_ore(self):
        return self.currentOre
    
    #return current fuel amount
    def get_current_fuel(self):
        return self.currentFuel
    
    #return loaded stauts
    def get_is_loaded(self):
        return self.currentOre > 0
    
    #set collecting status
    def set_is_collecting(self, value):
        self.is_collecting = value

    #return collecting status
    def get_is_collecting(self):
        return self.is_collecting
    
    #get refuling status
    def set_is_refueling(self, value):
        self.is_refueling = value
    
    #refuel tank
    def refuel(self):
        if not(self.currentFuel == self.maxFuel):
            if (self.maxFuel - self.currentFuel < int(0.05 * self.maxFuel)):
                self.currentFuel = self.maxFuel
            else:
                self.currentFuel += int(0.05 * self.maxFuel)
    
    #get keyboard imput from game management
    def set_moving(self, direction, moving = True):
        if moving:
            if direction == "LEFT":
                self.moving_left = True
            if direction == "RIGHT":
                self.moving_right = True
            if direction == "UP":
                self.moving_up = True
            if direction == "DOWN":
                self.moving_down = True
        else:
            if direction == "LEFT":
                self.moving_left = False
            if direction == "RIGHT":
                self.moving_right = False
            if direction == "UP":
                self.moving_up = False
            if direction == "DOWN":
                self.moving_down = False