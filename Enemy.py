# -*- coding: utf-8 -*-
from Entity import Entity
import pygame 
from pygame.locals import *

class Enemy(Entity):
    
    direction = 0
    def __init__(self, x, y, skin):
        Entity.__init__(self)
        self.skin = skin
        self.image = pygame.image.load(self.skin+"/enemy_right.png")
        self.image = pygame.transform.scale(self.image, (55, 72))
        self.image.convert()
        self.rect = Rect(x, y, 55, 72)  #Платформата се извежда
        self.xvel = 1              
        self.yvel = 0
        self.onGround = False
        self.hitPlatform = False
    
    def update(self, move, platforms, max_height):        #Функция за ъпдейтване на състоянието на играча
        if move:  
            if (self.direction%2 ==0):  #Провери за предишното състояние
                self.image = pygame.image.load(self.skin+"/enemy_right.png")
                self.image = pygame.transform.scale(self.image, (55, 72))
            else:
                self.image = pygame.image.load(self.skin+"/enemy_left.png")
                self.image = pygame.transform.scale(self.image, (55, 72))
        if not self.onGround:    # Създаване на гравитация
            self.yvel += 0.3
            if self.yvel > 100: self.yvel = 100
                
        
        # Измести играча по X
        self.rect.left += self.xvel
        # Колизия по Х
        self.collide(self.xvel, 0, platforms, max_height)
        # Измести играча по Y
        self.rect.top += self.yvel
        # Играча не се намира на платформа
        self.onGround = False;
        # Колизия по Y
        self.collide(0, self.yvel, platforms, max_height)
        
    
    def collide(self, xvel, yvel, platforms, max_height):   #Функция, проверяваща за колизии 
        for p in platforms:
            if pygame.sprite.collide_rect(self, p): 
                if xvel > 0:
                    self.rect.right = p.rect.left
                    self.xvel *= -1
                    self.direction +=1
                if xvel < 0:
                    self.rect.left = p.rect.right
                    self.xvel *= -1
                    self.direction +=1
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.hitPlatform = False  
                    self.yvel = 0          
                if yvel < 0:
                    self.rect.top = p.rect.bottom 
                    self.hitPlatform = True 
                    self.onGround = False
                    self.yvel = 0 
