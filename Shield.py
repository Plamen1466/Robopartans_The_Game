# -*- coding: utf-8 -*-
from Entity import Entity
import pygame 
from pygame.locals import *


class Shield(Entity):
    width = 32
    height = 32
    def __init__(self, x, y, image_path):
        Entity.__init__(self)
        self.image = pygame.image.load(image_path+"/shield.png")
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = Rect(x, y, self.width, self.height)
    def hide(self):
        self.image.fill(((153,255,0, 0))) #Цвета става като този на фона и се задава пълна прозрачност
