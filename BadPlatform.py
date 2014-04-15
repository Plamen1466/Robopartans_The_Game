# -*- coding: utf-8 -*-
from Entity import Entity
import pygame 
from pygame.locals import *

class Bad_Platform(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = pygame.image.load("files/Platforms/Bad_Platform.png")
        self.image = pygame.transform.scale(self.image, (128, 32))
        self.image.convert()
       
        self.rect = Rect(x, y+10, 128, 32)  #Платформата се извежда "вкопана"

