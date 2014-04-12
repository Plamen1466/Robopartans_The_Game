from Entity import Entity
import pygame 
from pygame.locals import *


class Target(Entity):
    width = 32
    height = 32
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = pygame.image.load("files/Platforms/Gears/gear_16.png")
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = Rect(x, y, self.width, self.height)
    def hide(self):
        self.image.fill(((153,255,0, 0)))
