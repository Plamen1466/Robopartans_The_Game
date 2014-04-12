# -*- coding: utf-8 -*-
import pygame, pygame.mixer
import subprocess
from pygame.locals import * 
from pygame import *

WIN_WIDTH = 1200
WIN_HEIGHT = 705
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 32
FLAGS = 0
CAMERA_SLACK = 30

def game():
    global cameraX, cameraY
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY, pygame.FULLSCREEN)
    pygame.display.set_caption("Robopartans: The Game V1.2")
    timer = pygame.time.Clock()

    up = down = left = right = running = False
    bg = Surface((32,32))
    #bg.convert()
    bg.fill((153,255,0))#ЦВЯТ НА ФОНА
    entities = pygame.sprite.Group()
    player = Player(55, 72)
    platforms = []

    x = y = 0
    level = [
        "SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
        "S                                                                                                S",
        "S                                                                                                S",
        "S                                                                                                S",
        "S                                                       T      T            T                    S",
        "S                                        T        T                   P-------                   S",
        "S                                      p---                                                      S",
        "S                                                      T                                         S",
        "S                                                    p---                    T                   S",
        "S                                 T                             T        P-------                S",
        "S                             P-------                        p---                       T       S",
        "S                                                 T                                    p---      S", 
        "S                T                            P-------                                           S",
        "S            P-------               T                                 p---                       S",
        "S                                  p---                       T                    T             S",
        "S                           T                              P-------             P-------         S",
        "S                         p---                                                                   S",
        "S                                                                                                S",
        "S                                            T                                                   S",
        "SG-----------G-----------G-----------G-----------G-----------G-----------G-----------G-----------S",
        "S                                                                                                S"]
    # build the level
    for row in level:
        for col in row:
            if col == "S":
                s = Score_line(x, y)
                platforms.append(s)
                entities.add(s)
            if col == "p":
                p = Platforms(x, y, 108, 32,"files/Platforms/Blue_beem_5_obrabotena.png")
                platforms.append(p)
                entities.add(p)
            if col == "P":
                P = Platforms(x, y, 251, 32,"files/Platforms/Blue_beem_11_obrabotena.png")
                platforms.append(P)
                entities.add(P)
            if col == "G":
                g = Ground(x, y)
                platforms.append(g)
                entities.add(g)
            if col == "T":
                t = Target(x, y)
                platforms.append(t)
                entities.add(t)
            if col == "B":
                t = Bad_Platforms(x, y)
                platforms.append(t)
                entities.add(t)
            
            x += 32
        y += 32
        x = 0
    y = 0
        
    
    total_level_width  = len(level[0])*32
    total_level_height = len(level)*32
    camera = Camera(total_level_width, total_level_height)
    entities.add(player)
    font = pygame.font.Font('files/Fonts/Adventure Subtitles.ttf',20)
    while 1:
        timer.tick(100)
        scoretext = font.render("Score:"+str(player.score)+"  Jumps:"+str(player.jumps)+ "   Lives:"+str(player.lives), 1,(255,255,255))

        for e in pygame.event.get():
            if e.type == QUIT: raise SystemExit, "QUIT"
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                menu_game()
            if e.type == KEYDOWN and e.key == K_SPACE:
                up = True
                
            if e.type == KEYDOWN and e.key == K_DOWN:
                down = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True

                
            if e.type == KEYUP and e.key == K_SPACE:
                up = False
            if e.type == KEYUP and e.key == K_DOWN:
                down = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
           

        # draw background
        for y in range(32):
            for x in range(64):
               screen.blit(bg, (x*32 , y*32))


        # update player, draw everything else
        
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        screen.blit(scoretext, (10 , 10))
        player.update(up, down, left, right, running, platforms)
        camera.update(player)##=========================================
        pygame.display.update()

class Camera(object):
    def __init__(self, width, height):
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):

		l, t, _, _ = target.rect
		_, _, w, h = self.state
		l, t, _, _ = -l+HALF_WIDTH, -t+HALF_HEIGHT, w, h

		l = min(0, l)                           # stop scrolling at the left edge
		l = max(-(self.state.width-WIN_WIDTH), l)   # stop scrolling at the right edge
		t = max(-(self.state.height-WIN_HEIGHT), t) # stop scrolling at the bottom
		t = min(0, t)                           # stop scrolling at the top
		self.state = Rect(l, t, w, h)
		return Rect(l, t, w, h)

#==================================================================================================

#==================================================================================================

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class Player(Entity):
    score = 0
    jumps = 0
    lives = 3
    

    def __init__(self, x, y):
        Entity.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.image = pygame.image.load("files/Skins/glaven.png")
        self.image = pygame.transform.scale(self.image, (55, 72))
        self.image.convert()
        self.rect = Rect(y, x, 55, 72)

    def update(self, up, down, left, right, running, platforms):
        if up:
            # only jump if on the ground
            if self.onGround:
                sound = pygame.mixer.Sound('files/Sounds/Mario_Jumping-Mike_Koenig-989896458.wav')
                sound.play()
                self.yvel -= 9
                self.jumps +=1
                
        if down:
            pass
        if left:
            self.xvel = -6
        if right:
            self.xvel = 6
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

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                
                    
                if isinstance(p, Target):
                    self.score+=16
                    platforms.remove(p)
                    p.hide()
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
        

#========================================================================================
class Score_line(Entity):          #Инициализира платформите и ограждащата рамка
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = pygame.image.load("files/Platforms/Platform_blue_plate.png")
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.image.convert()
       
        self.rect = Rect(x, y, 32, 32)

    def update(self):
        pass


class Ground(Entity):          #Инициализира платформите и ограждащата рамка
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = pygame.image.load("files/Platforms/Ready_project_Plamen_Dikov.png")
        self.image = pygame.transform.scale(self.image, (64*6, 64))
        self.image.convert()
       
        self.rect = Rect(x, y, 64*6, 64)

    def update(self):
        pass
    
class Platforms(Entity):      
    def __init__(self, x, y, width, height, image_path):
        Entity.__init__(self)
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = Rect(x, y, width, height)

    def update(self):
        pass

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
        


    def update(self):
        pass


#=========================================================================================
#class ExitBlock(Platform):
 #   def __init__(self, x, y):
  #      Platform.__init__(self, x, y)
   #     self.image.fill(Color("#0033FF"))

#if __name__ == "__main__":
#    game()

#============================================================================================================================================================================
#============================================================================================================================================================================
#============================================================================================================================================================================
#============================================================================================================================================================================

if not pygame.display.get_init():
    pygame.display.init()

if not pygame.font.get_init():
    pygame.font.init()


class Menu:
    lista = []
    pola = []
    rozmiar_fontu = 32
    font_path = 'files/Fonts/Adventure Subtitles.ttf'
    font = pygame.font.Font
    dest_surface = pygame.Surface
    ilosc_pol = 0
    pozycja_zaznaczenia = 0
    pozycja_wklejenia = (0,0)
    menu_width = 0
    menu_height = 0

    class Pole:
        tekst = ''
        pole = pygame.Surface
        pole_rect = pygame.Rect
        zaznaczenie_rect = pygame.Rect

    def move_menu(self, top, left):
        self.pozycja_wklejenia = (top,left) 

    def set_colors(self, text, selection, background):
        self.kolor_tla = background
        self.kolor_tekstu =  text
        self.kolor_zaznaczenia = selection
        
    def set_fontsize(self,font_size):
        self.rozmiar_fontu = font_size
        
    def set_font(self, path):
        self.font_path = path
        
    def get_position(self):
        return self.pozycja_zaznaczenia
    
    def init(self, lista, dest_surface):
        self.lista = lista
        self.dest_surface = dest_surface
        self.ilosc_pol = len(self.lista)
        self.stworz_strukture()        
        
    def draw(self,przesun=0):
        if przesun:
            self.pozycja_zaznaczenia += przesun 
            if self.pozycja_zaznaczenia == -1:
                self.pozycja_zaznaczenia = self.ilosc_pol - 1
            self.pozycja_zaznaczenia %= self.ilosc_pol
        menu = pygame.Surface((self.menu_width, self.menu_height))
        menu.fill(self.kolor_tla)
        zaznaczenie_rect = self.pola[self.pozycja_zaznaczenia].zaznaczenie_rect
        pygame.draw.rect(menu,self.kolor_zaznaczenia,zaznaczenie_rect)

        for i in xrange(self.ilosc_pol):
            menu.blit(self.pola[i].pole,self.pola[i].pole_rect)
        self.dest_surface.blit(menu,self.pozycja_wklejenia)
        return self.pozycja_zaznaczenia

    def stworz_strukture(self):
        przesuniecie = 0
        self.menu_height = 0
        self.font = pygame.font.Font(self.font_path, self.rozmiar_fontu)
        for i in xrange(self.ilosc_pol):
            self.pola.append(self.Pole())
            self.pola[i].tekst = self.lista[i]
            self.pola[i].pole = self.font.render(self.pola[i].tekst, 1, self.kolor_tekstu)

            self.pola[i].pole_rect = self.pola[i].pole.get_rect()
            przesuniecie = int(self.rozmiar_fontu * 0.2)

            height = self.pola[i].pole_rect.height
            self.pola[i].pole_rect.left = przesuniecie
            self.pola[i].pole_rect.top = przesuniecie+(przesuniecie*2+height)*i

            width = self.pola[i].pole_rect.width+przesuniecie*2
            height = self.pola[i].pole_rect.height+przesuniecie*2            
            left = self.pola[i].pole_rect.left-przesuniecie
            top = self.pola[i].pole_rect.top-przesuniecie

            self.pola[i].zaznaczenie_rect = (left,top ,width, height)
            if width > self.menu_width:
                    self.menu_width = width
            self.menu_height += height
        x = self.dest_surface.get_rect().centerx - self.menu_width / 2
        y = self.dest_surface.get_rect().centery - self.menu_height / 2
        mx, my = self.pozycja_wklejenia
        self.pozycja_wklejenia = (x+mx, y+my) 


def menu_game():
    import sys
#================ Промяна на иконата ===============================================
    icon = pygame.image.load("files/Skins/Martincho.png")
    icon = pygame.transform.scale(icon, (32, 32))
    pygame.display.set_icon(icon)
#================ Мишката не се вижда ==============================================
   # pygame.mouse.set_visible(0)
#================ В заглавната лента се извежда името на играта ====================
    pygame.display.set_caption("RBP_V1.2")

#================ Избор на размер на прозореца =====================================
    screen = pygame.display.set_mode((1300,650), pygame.FULLSCREEN) #0,6671875 and 0,(6) of HD resoultion
#================ Зареждане на фон =================================================
    background = pygame.image.load("files/Martinchovcite_menu1.png")
    background = pygame.transform.scale(background, (1450,805))
    screen.blit(background, (-80, -100))

    

#================ Пояснителен текст над менюто =====================================
   
    font=pygame.font.Font('files/Fonts/Adventure Subtitles.ttf',30)
    menutext=font.render("MENU", 1,(145,183,220))
    screen.blit(menutext, (677, 230))
#===================================================================================
    '''First you have to make an object of a *Menu class.
    *init take 2 arguments. List of fields and destination surface.
    Then you have a 4 configuration options:
    *set_colors will set colors of menu (text, selection, background)
    *set_fontsize will set size of font.
    *set_font take a path to font you choose.
    *move_menu is quite interseting. It is only option which you can use before 
    and after *init statement. When you use it before you will move menu from 
    center of your surface. When you use it after it will set constant coordinates. 
    Uncomment every one and check what is result!
    *draw will blit menu on the surface. Be carefull better set only -1 and 1 
    arguments to move selection or nothing. This function will return actual 
    position of selection.
    *get_postion will return actual position of seletion. '''
    menu = Menu()#necessary

#=============== Задаване на цветовете на фона, маркера и текста на менюто ========
    menu.set_colors((145,183,220),(36,36,168),(59,60,189))#optional
#=============== Задаване на размер на менюто =====================================
    menu.set_fontsize(30)#optional#=============== Задаване на позиция, където менюто ще бъде изведено ==============    
    menu.move_menu(75, 58)#optional
#=============== Инициализиране на съдържанието ===================================
    menu.init(['Start','Help','About','Quit'], screen)#necessary
#=============== Изчертаване на менюто ============================================
    menu.draw()#necessary
#==================================================================================


    pygame.key.set_repeat(199,69)#(delay,interval)
    
    pygame.display.update()
    
    while 1:
        
        for event in pygame.event.get():
            
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    menu.draw(-1)
                    #here is the Menu class function
                if event.key == K_DOWN:
                    menu.draw(1)
                    #here is the Menu class function
                if event.key == K_RETURN:
                    if menu.get_position() == 3:#here is the Menu class function
                        pygame.display.quit()
                        sys.exit()
                    if menu.get_position() == 0:
                        game()
                    if menu.get_position() == 1:
                        font_controls=pygame.font.Font('files/Fonts/Adventure Subtitles.ttf',25)
                        controls_text = font_controls.render("CONTROLS:", 1, (145, 183, 220))
                        screen.blit(controls_text, (20, 200))
                    if menu.get_position() == 2:
                        subprocess.Popen("python files/About.py")
                    
                if event.key == K_ESCAPE:
                    pygame.display.quit()
                    sys.exit()
                
                
                pygame.display.update()
            elif event.type == QUIT:
                pygame.display.quit()
                sys.exit()
        
        pygame.time.wait(8)
        
if __name__ == "__main__":
    menu_game()
