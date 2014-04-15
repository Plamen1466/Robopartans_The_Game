from Entity import Entity
import pygame 
from pygame.locals import *

class Platforms(Entity):      
    def __init__(self, x, y, width, height, image_path):
        Entity.__init__(self)
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = Rect(x, y, width, height)

