from gameObject import GameObject

class GasStation(GameObject):
    #initialize object
    def __init__(self, x, y, imageList, screen, font, sound):
        super().__init__(x, y, imageList, screen, font)
        self.sound = sound
        self.is_refueling = False
        self.sound_playing = False

    #implementation of abstract update method
    def update(self):
        if (self.is_refueling):
            if not(self.sound_playing):
                self.sound.play(loops=-1, maxtime=0)
                self.sound_playing = True
        else:
            if (self.sound_playing):
                self.sound.stop()
                self.sound_playing = False

    #implementation of abstract draw method
    def draw(self):
        self.screen.blit(self.current_image, self.rect)

    #set refueling status
    def set_is_refueling(self, value):
        self.is_refueling = value