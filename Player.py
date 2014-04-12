from Entity import Entity
import pygame 
from Target import Target
from Platforms import Platforms
from pygame.locals import *


class Player(Entity):
    score = 0
    jumps = 0
    lives = 3
    moving_left = False
    moving_right = False

    def __init__(self, x, y):
        Entity.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.image = pygame.image.load("files/Skins/martincho_right.png")
        self.image = pygame.transform.scale(self.image, (55, 72))
        self.image.convert()
        self.rect = Rect(y, x, 55, 72)

    def update(self, up, down, left, right, running, platforms):
        if up:
            # only jump if on the ground
            if self.onGround:
                sound = pygame.mixer.Sound('files/Sounds/Mario_Jumping-Mike_Koenig-989896458.wav')
                #sound.play()
                self.yvel -= 9
                self.jumps +=1
                
        if down:
            pass
        if left:
            self.xvel = -6
            if not self.moving_left:
                self.image = pygame.image.load("files/Skins/martincho_left.png")
                self.image = pygame.transform.scale(self.image, (55, 72))
                self.moving_left = True
                self.moving_right = False
        if right:
            self.xvel = 6
            if not self.moving_right:
                self.image = pygame.image.load("files/Skins/martincho_right.png")
                self.image = pygame.transform.scale(self.image, (55, 72))
                self.moving_right = True
                self.moving_left = False
        if not self.onGround:
            # only accelerate with gravity if in the air
            self.yvel += 0.3
            # max falling speed
            if self.yvel > 100: self.yvel = 100
        if not(left or right):
            self.xvel = 0
        # increment in x direction
        self.rect.left += self.xvel
        # do x-axis collisions
        self.collide(self.xvel, 0, platforms)
        # increment in y direction
        self.rect.top += self.yvel
        # assuming we're in the air
        self.onGround = False;
        # do y-axis collisions
        self.collide(0, self.yvel, platforms)
    """#====================================================================================================
            if self.rect.left > 200:
                self.rect.left = 40
    #===================================================================================================="""
    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if isinstance(p, Target):
                    self.score+=16
                    platforms.remove(p)
                    p.hide()
                else:
                    if xvel > 0:
                        self.rect.right = p.rect.left
                        print "collide right"
                    if xvel < 0:
                        self.rect.left = p.rect.right
                        print "collide left"
                    if yvel > 0:
                        self.rect.bottom = p.rect.top
                        self.onGround = True
                        self.yvel = 0
                    if yvel < 0:
                        self.rect.top = p.rect.bottom   
