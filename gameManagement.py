import pygame
from pygame import mixer
import math
from button import Button
from inputField import InputField
from startingPoint import StartingPoint
from endPoint import EndPoint
from gasStation import GasStation
from truck import Truck
from helicopter import Helicopter

class GameManagement():
    #define constants
    MODE_START = 'START'
    MODE_RUNNING = 'RUNNING'
    MODE_END = 'END'

    #initialize object
    def __init__(self):
        #initialize pygame and set dynamic game window size
        pygame.init()
        mixer.init()

        display_info = pygame.display.Info()
        SCREEN_WIDTH = display_info.current_w
        SCREEN_HEIGHT = display_info.current_h

        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('The TransportGame')

        self.screen = screen
        self.screen_w = screen.get_width()
        self.screen_h = screen.get_height()
        self.scaling = self.screen_w / 1600
        self.font = pygame.font.SysFont("Arial" , round(20 * self.scaling) , bold = True)

        #set framerate
        self.clock = pygame.time.Clock()
        self.FPS = 60

        #init state variables
        self.mode = self.MODE_START
        self.end_state = 0
        self.sound_muted = False

        self.init_game_variables()
        self.load_sounds()
        self.load_images()
        #call after resources are loaded
        self.initialize_objects()

    #reset game variables, objects and state
    def restart_game(self):
        self.init_game_variables()
        self.initialize_objects()

        self.mode = self.MODE_START
        self.end_state = 0

        #reset sounds and music
        mixer.stop()
        mixer.music.load('audio/music.mp3')
        mixer.music.set_volume(0.3)
        mixer.music.play(-1, 0.0, 5000)

    #set starting values for game variables
    def init_game_variables(self):
        self.capacity_truck = 200
        self.consumption_truck = 20
        self.max_fuel_truck = 5000
        self.starting_amount_ore = 4000
        self.speed_truck = 4
        self.speed_helicopter = 5
        self.win_percent = 80

    #load sound files
    def load_sounds(self):
        self.victory_fx = self.load_sound('audio/victory.mp3', 0.3)
        self.lose_fx = self.load_sound('audio/game_over.mp3', 0.3)
        self.helicopter_fx = self.load_sound('audio/helicopter.mp3', 0.3)
        self.truck_fx = self.load_sound('audio/truck.mp3', 0.2)
        self.refuel_fx = self.load_sound('audio/refuel.mp3', 1)
        self.load_fx = self.load_sound('audio/load.mp3', 1)
        self.unload_fx = self.load_sound('audio/unload.mp3', 0.3)
        self.ore_stolen_fx = self.load_sound('audio/evil_laugh.mp3', 0.5)

    def load_sound(self, path, volume):
        sound = mixer.Sound(path)
        sound.set_volume(volume)
        return sound
    
    #load image files
    def load_images(self):
        #background
        banner_img = pygame.image.load('img/Background/banner2.png').convert_alpha()
        self.banner_img = pygame.transform.scale(banner_img, (self.screen_w, self.screen_h))

        ground1_img = pygame.image.load('img/Background/ground1.png').convert_alpha()
        self.ground1_img = pygame.transform.scale_by(ground1_img, self.scaling)
        #ui elements
        start_button_img = pygame.image.load('img/PlayButton.png').convert_alpha().subsurface((200, 140, 670, 410)) 
        self.start_button_img = pygame.transform.scale_by(start_button_img, (self.scaling * 0.2))

        restart_button_img = pygame.image.load('img/restart.png').convert_alpha()
        self.restart_button_img = pygame.transform.scale_by(restart_button_img, (self.scaling * 0.2))

        wasd_image = pygame.image.load('img/keyboard_keys.png').convert_alpha().subsurface((0, 0, 95, 60)) 
        self.wasd_image = pygame.transform.scale_by(wasd_image, (self.scaling * 2))
        #objects
        self.starting_point_img_list = []
        for i in range(1,24):
            starting_point_img = pygame.image.load(f'img/mine/{i}.png').convert_alpha().subsurface((20, 120, 260, 190))
            self.starting_point_img_list.append(pygame.transform.scale_by(starting_point_img, self.scaling))

        end_point_img = pygame.image.load('img/warehouse.png').convert_alpha()
        self.end_point_img = pygame.transform.scale_by(end_point_img, (self.scaling * 1.3))

        gas_station_img = pygame.image.load('img/gas_station.png').convert_alpha()
        self.gas_station_img = pygame.transform.scale_by(gas_station_img, (self.scaling * 0.5))

        truck_img = pygame.image.load('img/truck1.png').convert_alpha()
        self.truck_img = pygame.transform.scale_by(truck_img, (self.scaling * 0.5)) 

        #assets surface
        helicopter_assets = pygame.image.load('img/chopper.png').convert_alpha()
        
        helicopter_img = helicopter_assets.subsurface((44, 0, 44, 99))
        helicopter_img = pygame.transform.rotate(helicopter_img, 90)
        self.helicopter_img = pygame.transform.scale_by(helicopter_img, self.scaling) 
        
        helicopter_rotor_img = helicopter_assets.subsurface((132, 99, 96, 99))
        self.helicopter_rotor_img = pygame.transform.scale_by(helicopter_rotor_img, self.scaling)

    #initialize imported objects
    def initialize_objects(self):
        #create ui elements
        self.start_button = Button(self.screen.get_width() / 2, (0.8 * self.screen_h), self.start_button_img, self.screen)

        self.restart_button = Button(self.screen.get_width() / 2, (0.8 * self.screen_h), self.restart_button_img, self.screen)

        self.input_field_list = []

        self.input_capacity_truck = InputField(self.screen.get_width() / 2, (0.45 * self.screen_h), (200 * self.scaling), (32 * self.scaling), 16, self.screen, self.font, "Capacity",str(self.capacity_truck))
        self.input_field_list.append(self.input_capacity_truck)

        self.input_consumption_truck = InputField(self.screen.get_width() / 2, (0.5 * self.screen_h), (200 * self.scaling), (32 * self.scaling), 16, self.screen, self.font, "Consumption",str(self.consumption_truck))
        self.input_field_list.append(self.input_consumption_truck)

        self.input_starting_ore = InputField(self.screen.get_width() / 2, (0.55 * self.screen_h), (200 * self.scaling), (32 * self.scaling), 16, self.screen, self.font, "Starting Ore", str(self.starting_amount_ore))
        self.input_field_list.append(self.input_starting_ore)

        self.input_speed_truck = InputField(self.screen.get_width() / 2, (0.6 * self.screen_h), (200 * self.scaling), (32 * self.scaling), 16, self.screen, self.font, "Speed Truck", str(self.speed_truck))
        self.input_field_list.append(self.input_speed_truck)

        self.input_speed_helicopter = InputField(self.screen.get_width() / 2, (0.65 * self.screen_h), (200 * self.scaling), (32 * self.scaling), 16, self.screen, self.font, "Speed Helicopter", str(self.speed_helicopter))
        self.input_field_list.append(self.input_speed_helicopter)

        self.input_win_percent = InputField(self.screen.get_width() / 2, (0.7 * self.screen_h), (200 * self.scaling), (32 * self.scaling), 16, self.screen, self.font, "Win Percent", str(self.win_percent))
        self.input_field_list.append(self.input_win_percent)
        
        #create game objects
        self.starting_point = StartingPoint((0.09375 * self.screen_w), (0.75 * self.screen_h), self.starting_point_img_list, self.screen, self.font, self.load_fx, self.starting_amount_ore)

        self.end_point = EndPoint((0.92 * self.screen_w), (0.2 * self.screen_h), [self.end_point_img], self.screen, self.font)

        self.gas_station = GasStation((0.92 * self.screen_w), (0.86 * self.screen_h), [self.gas_station_img], self.screen, self.font, self.refuel_fx)

        self.truck = Truck((0.125 * self.screen_w), (0.33 * self.screen_h), [self.truck_img], self.screen, self.font, self.truck_fx, self.speed_truck, self.capacity_truck, self.max_fuel_truck, self.consumption_truck)

        self.helicopter = Helicopter((0.25 * self.screen_w), (0.66 * self.screen_h), [self.helicopter_img, self.helicopter_rotor_img], self.screen, self.font, self.helicopter_fx, self.speed_helicopter, self.truck)

    #draw background dynamically
    def draw_bg(self):
        if (self.mode == self.MODE_START):
            self.screen.blit(self.banner_img, (0, 0))

            #controls image
            self.screen.blit(self.wasd_image, (1200 * self.scaling, self.screen_h / 2))
            controls_img_size = self.wasd_image.get_size()

            controls__left_label = "Left"
            controls_left_txt = self.font.render(controls__left_label, 1, pygame.Color("Red"))
            self.screen.blit(controls_left_txt, ((1200 * self.scaling) - self.font.size(controls__left_label)[0], (self.screen_h / 2) + (controls_img_size[1] / 2)))

            controls_right_label = "Right"
            controls_right_txt = self.font.render(controls_right_label, 1, pygame.Color("Red"))
            self.screen.blit(controls_right_txt, ((1205 * self.scaling) + controls_img_size[0], (self.screen_h / 2) + (controls_img_size[1] / 2)))

            controls_up_label = "Up"
            controls_up_txt = self.font.render(controls_up_label, 1, pygame.Color("Red"))
            self.screen.blit(controls_up_txt, ((1200 * self.scaling) + (controls_img_size[0] / 2) - (self.font.size(controls_up_label)[0] / 2), (self.screen_h / 2) - (20 * self.scaling)))

            controls_down_label = "Down"
            controls_down_txt = self.font.render(controls_down_label, 1, pygame.Color("Red"))
            self.screen.blit(controls_down_txt, ((1200 * self.scaling) + (controls_img_size[0] / 2) - (self.font.size(controls_down_label)[0] / 2), (self.screen_h / 2) + (controls_img_size[1] + 5)))

        elif (self.mode == self.MODE_END):
            self.screen.fill('Grey')
        elif (self.mode == self.MODE_RUNNING):
            width = self.ground1_img.get_width()
            count_x = math.ceil(self.screen_w / width)
            count_y = math.ceil(self.screen_h / width)
            for y in range(0, count_y + 1):
                for x in range(0, count_x + 1):
                    self.screen.blit(self.ground1_img, (width * x, width * y))

    #draw game counter
    def draw_counter(self, truck):
        #fuel counter
        fuel_counter_txt = self.font.render(("Fuel: " + str(truck.get_current_fuel())), 1, pygame.Color("WHITE"))
        self.screen.blit(fuel_counter_txt, (0, 0))
        #ore counter
        ore_counter_txt = self.font.render(("Current Ore: " + str(truck.get_current_ore())), 1, pygame.Color("WHITE"))
        self.screen.blit(ore_counter_txt, (0, self.scaling * 15))
        #win counter
        win_counter_txt = self.font.render(("Goal: " + str(self.end_point.get_amount_ore()) + '/' + str(self.win_percent * self.starting_amount_ore // 100)), 1, pygame.Color("WHITE"))
        self.screen.blit(win_counter_txt, (0, self.scaling * 30))

    #check input fields for invalid values
    def check_inputs(self):
        can_start = True
        for field in self.input_field_list:
            if (field.get_text() == ''):
                field.toggle_error()
                can_start = False
        if not(can_start):
            return False

        if (int(self.input_capacity_truck.get_text()) > int(self.input_starting_ore.get_text()) / 4):
            self.input_capacity_truck.toggle_error()
            can_start = False
        if (int(self.input_speed_truck.get_text()) >= int(self.input_speed_helicopter.get_text())):
            self.input_speed_truck.toggle_error()
            can_start = False
        if (int(self.input_win_percent.get_text()) < 0 or int(self.input_win_percent.get_text()) > 100):
            self.input_win_percent.toggle_error()
            can_start = False
        return can_start
    
    #get data from input fields
    def set_input_data(self):
        self.capacity_truck = int(self.input_capacity_truck.get_text())
        self.truck.set_capacity(self.capacity_truck)
        self.consumption_truck = int(self.input_consumption_truck.get_text())
        self.truck.set_consumption(self.consumption_truck)
        self.starting_amount_ore = int(self.input_starting_ore.get_text())
        self.starting_point.set_amount_ore(self.starting_amount_ore)
        self.speed_truck= int(self.input_speed_truck.get_text()) * self.scaling #speed is also scaled according to display size
        self.truck.set_speed(self.speed_truck)
        self.speed_helicopter = int(self.input_speed_helicopter.get_text()) * self.scaling #speed is also scaled according to display size
        self.helicopter.set_speed(self.speed_helicopter)
        self.win_percent = int(self.input_win_percent.get_text())

    #check object collisions and react accordingly
    def check_collisions(self):
        #reset states
        self.truck.set_is_collecting(False)
        self.truck.set_is_refueling(False)
        self.starting_point.set_is_loading(False)
        self.gas_station.set_is_refueling(False)
        #collision with gas station
        if (self.truck.get_rect().colliderect(self.gas_station.get_rect())):
            self.truck.set_is_refueling(True)
            self.gas_station.set_is_refueling(True)
        #collision with starting point
        if (self.truck.get_rect().colliderect(self.starting_point.get_rect())):
            self.truck.set_is_collecting(True)
            if (self.truck.get_current_ore() < self.truck.get_capacity()):
                amountOre = self.starting_point.collect_ore(int(self.truck.get_capacity() * 0.2))
                self.truck.collect_ore(amountOre)
                self.starting_point.set_is_loading(True)
        #collision with end point
        if (self.truck.get_rect().colliderect(self.end_point.get_rect())):
            if (self.truck.get_current_ore() > 0):
                self.end_point.deposit_ore(self.truck.get_current_ore())
                self.truck.reset_ore()
                self.unload_fx.play()
        #collision with helicopter
        if (self.helicopter.get_rect().colliderect(self.truck.get_rect())):
            stolen_ore = self.truck.reset_ore()
            self.helicopter.steal_ore(stolen_ore)
            self.ore_stolen_fx.play()

    #check goal and update game state
    def check_goal(self):
        if (self.end_point.get_amount_ore() >= (self.win_percent * self.starting_amount_ore // 100)):
            self.mode = self.MODE_END
            self.end_state = 0
            self.terminate_running_actions()
        elif (self.helicopter.get_stolen_ore() > self.starting_amount_ore - (self.win_percent * self.starting_amount_ore // 100)):
            self.mode = self.MODE_END
            self.end_state = 1
            self.terminate_running_actions()
        elif not(self.truck.get_alive()):
            self.mode = self.MODE_END
            self.end_state = 2
            self.terminate_running_actions()

    #terminate running actions
    def terminate_running_actions(self):
        self.truck.kill()
        self.helicopter.kill()
        self.refuel_fx.stop()
        self.refuel_sound_playing = False
        
    #game loop
    def run(self):
        #music and sounds
        mixer.music.load('audio/music.mp3')
        mixer.music.set_volume(0.3)
        mixer.music.play(-1, 0.0, 5000)

        #run game
        run = True
        while run:
            self.clock.tick(self.FPS)

            #main menu
            if self.mode == self.MODE_START:
                #draw ui
                self.draw_bg()
                for field in self.input_field_list:
                    field.draw()
                self.start_button.draw()
                #process events
                for event in pygame.event.get():
                    #quit game
                    if event.type == pygame.QUIT:
                        run = False
                    #mouseclick
                    if event.type == pygame.MOUSEBUTTONDOWN: 
                        for field in self.input_field_list:
                            if (field.get_rect().collidepoint(event.pos)):
                                field.set_active(True)
                            else:
                                field.set_active(False)
                        if (self.start_button.get_rect().collidepoint(event.pos)):
                            if (self.check_inputs()):
                                self.set_input_data()
                                mixer.music.stop()
                                self.mode = self.MODE_RUNNING  
                    #keyboard pressed
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            run = False
                        # Check for backspace 
                        if event.key == pygame.K_BACKSPACE: 
                            for field in self.input_field_list:
                                if (field.get_active()):
                                    field.toggle_backspace()
                        else:
                            try:
                                if chr(event.key).isdigit():
                                    for field in self.input_field_list:
                                        if (field.get_active()):
                                            field.add_symbol(chr(event.key))
                            except ValueError:
                                return
                            
            #end screen
            elif self.mode == self.MODE_END:
                self.draw_bg()
                self.restart_button.draw()
                text = ''
                if (self.end_state == 0):
                    text = 'You won!!!'
                elif (self.end_state == 1):
                    text = 'You lost! The Ore was stolen'
                elif (self.end_state == 2):
                    text = 'You lost! Ran out of fuel'
                text_size = self.font.size(text)
                text_element = self.font.render(text, True, pygame.Color('WHITE'))
                self.screen.blit(text_element, ((self.screen_w / 2) - (text_size[0] / 2), self.screen_h / 2))
                if (self.end_state == 0):
                    self.victory_fx.play()
                else:
                    self.lose_fx.play()

                #process events
                for event in pygame.event.get():
                    #quit game
                    if event.type == pygame.QUIT:
                        run = False
                    #mouseclick
                    if event.type == pygame.MOUSEBUTTONDOWN: 
                        if (self.restart_button.get_rect().collidepoint(event.pos)):
                            self.restart_game()    
                    #keyboard pressed
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            run = False
            #game screen
            elif self.mode == self.MODE_RUNNING:
                #draw ui
                self.draw_bg()
                self.draw_counter(self.truck)
                #update objects
                self.starting_point.update()
                self.gas_station.update()
                self.truck.update()
                self.helicopter.update()
                #draw objects
                self.starting_point.draw()
                self.end_point.draw()
                self.gas_station.draw()
                self.truck.draw()
                self.helicopter.draw()
                #check collisions
                self.check_collisions()
                self.check_goal()
                #process events
                for event in pygame.event.get():
                    #quit game
                    if event.type == pygame.QUIT:
                        run = False
                    #keyboard pressed
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_a:
                            self.truck.set_moving("LEFT")
                        if event.key == pygame.K_d:
                            self.truck.set_moving("RIGHT")
                        if event.key == pygame.K_w:
                            self.truck.set_moving("UP")
                        if event.key == pygame.K_s:
                            self.truck.set_moving("DOWN")
                        if event.key == pygame.K_ESCAPE:
                            run = False
                    #keyboard released
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_a:
                            self.truck.set_moving("LEFT", False)
                        if event.key == pygame.K_d:
                            self.truck.set_moving("RIGHT", False)
                        if event.key == pygame.K_w:
                            self.truck.set_moving("UP", False)
                        if event.key == pygame.K_s:
                            self.truck.set_moving("DOWN", False)

            pygame.display.update()     

        pygame.quit()