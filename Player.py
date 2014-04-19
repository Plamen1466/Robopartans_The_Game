# -*- coding: utf-8 -*-
from Entity import Entity
import pygame 
from Target import Target
from Platforms import Platforms
from BadPlatform import Bad_Platform
from pygame.locals import *


class Player(Entity):  
    score = 0             #Задаване на член променливи за точки, колела, които трябва да се съберат, скокове, животи и посока на движение
    gears_count = 0
    jumps = 0
    lives = 3
    moving_left = False
    moving_right = False

    def __init__(self, x, y, skin):       #Конструктор
        Entity.__init__(self)
        self.xvel = 0               
        self.yvel = 0
        self.skin = skin
        self.onGround = False
        self.hitPlatform = False
        self.image = pygame.image.load(self.skin+"/martincho_left.png")
        self.image = pygame.transform.scale(self.image, (55, 72))
        self.image.convert()
        self.rect = Rect(y, x, 55, 72)

    def update(self, up, left, right, running, platforms):        #Функция за ъпдейтване на състоянието на играча
        if up:  #Скок
            # Скочи само ако си на платформа
            if self.onGround:
                jump_sound = pygame.mixer.Sound('files/Sounds/jump.wav')    #Изпълни звук
                jump_sound.play()
                if not self.hitPlatform:    #Ако по време на скока се удариш в платформа, започни да падаш
                    self.yvel -= 9                
                self.jumps +=1              #Увеличи брояча на скокове с 1

        if left: #Движение наляво  
            self.xvel = -6
            if not self.moving_left:  #Провери за предишното състояние
                self.image = pygame.image.load(self.skin+"/martincho_left.png") #Зареди съответната картинка
                self.image = pygame.transform.scale(self.image, (55, 72))
                self.moving_left = True     
                self.moving_right = False
        if right:   #Движение надясно
            self.xvel = 6
            if not self.moving_right:   #Провери за предишното състояние
                self.image = pygame.image.load(self.skin+"/martincho_right.png")   #Зареди съответната картинка
                self.image = pygame.transform.scale(self.image, (55, 72))
                self.moving_right = True
                self.moving_left = False
        if not self.onGround:    # Създаване на гравитация
            self.yvel += 0.3
            if self.yvel > 100: self.yvel = 100
        if not(left or right):  #Ако не се движа наляво или надясно, задай скорост 0 по оста Х
            self.xvel = 0
        # Измести играча по X
        self.rect.left += self.xvel
        # Колизия по Х
        self.collide(self.xvel, 0, platforms)
        # Измести играча по Y
        self.rect.top += self.yvel
        # Играча не се намира на платформа
        self.onGround = False;
        # Колизия по Y
        self.collide(0, self.yvel, platforms)
    
    def collide(self, xvel, yvel, platforms):   #Функция, проверяваща за колизии 
        for p in platforms:
            if pygame.sprite.collide_rect(self, p): 
                if isinstance(p, Target):       #Ако играча е в рамките на зъбно колело
                    p.hide()                    #Зъбното колело изчезва
                    self.score+=16              #Вдига се брояча на точките
                    platforms.remove(p)         #Премахва се от списъка с платформи
                    gear_sound = pygame.mixer.Sound('files/Sounds/gear.wav')    
                    gear_sound.play()           #Изпълнява се съответния звук

                elif isinstance(p, Bad_Platform):   #Ако играча е в рамките на платформа, която го убива
                    self.lives-=1                   #Намаляват се животите с 1
                    pain_sound = pygame.mixer.Sound('files/Sounds/pain.wav')
                    pain_sound.set_volume(0.05)
                    pain_sound.play()               #Изпълнява се съответния звук
                    pygame.time.delay(1000)         #Изчаква се 1 секунда
                    self.rect.left = 40             #Играчът се връща в началото на нивото
                    self.rect.top = 40
                else:                               #В останалите случаи променяй състоянието на играча 
                    if xvel > 0:
                        self.rect.right = p.rect.left
                    if xvel < 0:
                        self.rect.left = p.rect.right
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
