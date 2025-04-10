import pygame
from gameObject import GameObject

class Helicopter(GameObject):
    #initialize object
    def __init__(self, x, y, imageList, screen, font, sound, speed, truck):
        super().__init__(x, y, imageList, screen, font)
        self.sound = sound
        self.speed = speed
        self.truck = truck
        self.current_rotor_img = self.imageList[1]
        self.alive = True
        self.rotor_state = 0
        self.facing_right = True
        self.animation_cooldown = 5
        self.chasing = True
        self.home_x = screen.get_width() / 2
        self.home_y = -200
        self.cooldown = 0
        self.stolen_ore = 0
        self.sound_playing = False

    #implementation of abstract update method
    def update(self):
        if (self.alive):
            if (self.cooldown == 0):
                dx = 0
                dy = 0
                is_trailing = False
                own_position = self.rect.center
                #update destination
                destination_position = (0, 0)
                if (self.chasing):
                    destination_position = self.truck.get_rect().center
                    if (not self.truck.get_is_loaded() or self.truck.get_is_collecting()):
                        is_trailing = True
                        coord = list(destination_position)
                        if (own_position[0] < coord[0]):
                            coord[0] -= 300
                            self.facing_right = True
                        else:
                            coord[0] += 300
                            self.facing_right = False
                        if (own_position[1] < coord[1]):
                            coord[1] -= 100
                        else:
                            coord[1] += 100
                        destination_position = tuple(coord)
                else:
                    destination_position = (self.home_x, self.home_y)

                #chase destination
                dy_to_destination = destination_position[1] - own_position[1]
                if (dy_to_destination > 0):
                    if (dy_to_destination < self.speed):
                        dy += dy_to_destination
                    else:
                        dy += self.speed
                if (dy_to_destination < 0):
                    if (dy_to_destination > -self.speed):
                        dy += dy_to_destination
                    else:
                        dy -= self.speed
                dx_to_destination = destination_position[0] - own_position[0]
                if (dx_to_destination > 0):
                    if (dx_to_destination < self.speed):
                        dx = dx_to_destination
                    else:
                        dx += self.speed
                if (dx_to_destination < 0):
                    if (dx_to_destination > -self.speed):
                        dx += dx_to_destination
                    else:
                        dx -= self.speed
                    
                #apply changes to position and displayed image
                if not(is_trailing):
                    if (dx > 0):
                        self.facing_right = True
                    if (dx < 0):
                        self.facing_right = False
                if (self.facing_right):
                    self.current_image = pygame.transform.rotate(self.imageList[self.image_counter], 180)
                else:
                    self.current_image = self.imageList[self.image_counter]

                self.rect.x += dx
                self.rect.y += dy

                if not(self.sound_playing):
                    self.sound.play(loops=-1, maxtime=0) # Loops indefinitely
                    self.sound_playing = True

                #homespot reached
                if (not self.chasing and destination_position == own_position):
                    self.chasing = True
                    self.sound.stop()
                    self.sound_playing = False
                    self.cooldown = 1800

                #animate rotor
                if (self.animation_cooldown == 0):
                    if (self.rotor_state == 0):
                        self.current_rotor_img = self.imageList[1]
                        self.rotor_state = 1
                    else:
                        self.current_rotor_img = pygame.transform.rotate(self.imageList[1], 45)
                        self.rotor_state = 0
                    self.animation_cooldown = 5
                else:
                    self.animation_cooldown -= 1
            else:
                self.cooldown -= 1

    #implementation of abstract draw method
    def draw(self):
        rotor_rect = self.current_rotor_img.get_rect()
        rotor_rect.center = (self.rect.center)

        self.screen.blit(self.current_image, self.rect)
        self.screen.blit(self.current_rotor_img, rotor_rect)

    #stop all actions
    def kill(self):
        self.alive = False
        self.sound.stop()
        self.sound_playing = False

    #set speed
    def set_speed(self, speed):
        self.speed = speed

    #steal ore from player
    def steal_ore(self, stolen_ore):
        self.stolen_ore += stolen_ore
        self.chasing = False

    #return total amount of stolen ore
    def get_stolen_ore(self):
        return self.stolen_ore

    #deposit stolen ore
    def deposit_ore(self):
        self.chasing  = True