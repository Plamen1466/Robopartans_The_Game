from Entity import Entity
import pygame 
from pygame.locals import *

class Score_line(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = pygame.image.load("files/Platforms/Platform_blue_plate.png")
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.image.convert()
       
        self.rect = Rect(x, y, 32, 32)

    def update(self):
        pass
