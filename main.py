import pygame
from pygame import mixer
from gameManagement import GameManagement

mixer.init()
pygame.init()

display_info = pygame.display.Info()
SCREEN_WIDTH = display_info.current_w
SCREEN_HEIGHT = display_info.current_h

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('The TransportGame')

game_management = GameManagement.__new__(GameManagement)
game_management.__init__(screen)

game_management.initialize_objects()
game_management.run()