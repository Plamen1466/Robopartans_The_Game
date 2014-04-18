# -*- coding: utf-8 -*-
import pygame, pygame.mixer
import subprocess
from Entity import Entity
from ScoreLine import Score_line
from Camera import Camera
from Ground import Ground
from Player import Player
from BadPlatform import Bad_Platform
from Platforms import Platforms
from Target import Target
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

def game(file_level):
    global cameraX, cameraY
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY, pygame.FULLSCREEN)            #Създаване на прозореца, задаване на fullscreen
    pygame.display.set_caption("Robopartans: The Game V1.2")                #Задаване на име на прозореца
    lives_image = pygame.image.load("files/Skins/helmet.png")               #Задаване на картинка, която ще илюстрира животите на играча
    lives_image = pygame.transform.scale(lives_image, (32, 32))             
    
    timer = pygame.time.Clock()                               #Инициализация на таймера                 
    pygame.mouse.set_visible(0)                               #Мишката не се вижда р рамките на прозореца
    up = left = right = running = False                       #Всички функции за движение са неактивни

    bg = Surface((32,32))                                     #Създаване на фона
    bg.fill((153,255,0))                                      #Цвят на фона
    entities = pygame.sprite.Group()
    player = Player(55, 72)                                   #Създаване на играча от класа Player
    platforms = []                                            #Инициализация на списък, в който ще се съхраняват всички активни платформи 

    x = y = 0 
    f = open(file_level)                                                
    level = f.readlines()
    f.close()

    for row in level:                   #Всички моделирани елементи се добавят в списъка с активните платформи
        for col in row:
            if col == "S":
                s = Score_line(x, y)
                platforms.append(s)
                entities.add(s)
            if col == "p":
                p = Platforms(x, y, 108, 32,"files/Platforms/Blue_beem_5.png")
                platforms.append(p)
                entities.add(p)
            if col == "P":
                P = Platforms(x, y, 251, 32,"files/Platforms/Blue_beem_11.png")
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
                player.gears_count += 1
            if col == "B":
                b = Bad_Platform(x, y)
                platforms.append(b)
                entities.add(b)
            
            x += 32
        y += 32
        x = 0
    y = 0
        
    
    total_level_width  = (len(level[0])-2)*32                               
    total_level_height = len(level)*32
    camera = Camera(total_level_width, total_level_height)
    entities.add(player)                                                                        
    font = pygame.font.Font('files/Fonts/Adventure Subtitles.ttf',20)       #Форматиране на текста в score line-а 
    while 1:
        timer.tick(120)
    
        #Пояснителен текст        
        lives_text = font.render("LIVES:", 1,(255,255,255))
        
        for e in pygame.event.get():                     #Проверка за натиснати бутони 
            if e.type == QUIT: raise SystemExit, "QUIT"
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                menu_game()
            if e.type == KEYDOWN and e.key == K_SPACE:
                up = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True

                
            if e.type == KEYUP and e.key == K_SPACE:
                up = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
           

        # Извеждане на фона
        for y in range(32):
            for x in range(64):
               screen.blit(bg, (x*32 , y*32))
        
        #Текст, който показва прогреса по събиране на точки и броя скокове, които са направени


        # Ъпдейтване на играча и извеждане на всичко останало
        player.update(up, left, right, running, platforms)
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        camera.update(player, WIN_WIDTH, WIN_HEIGHT)

        screen.blit(lives_text, (900 , 4))

        for i in range(player.lives):
            screen.blit(lives_image, ((1050 - i*35), 0)) 
        #Текст, който показва прогреса по събиране на точки и броя скокове, които са направени
        scoretext = font.render("Score:"+str(player.score)+"/"+str(player.gears_count*16)+"  Jumps:"+str(player.jumps), 1,(255,255,255))
        screen.blit(scoretext, (10 , 4))
 

        #Проверка дали играта е свършила
        if player.score == player.gears_count*16: #Ако са събрани всички зъбни колела, изведи съобщение и се върни в началното меню        
            font_end = pygame.font.Font('files/Fonts/Adventure Subtitles.ttf',30)
            end_text_first_line = font_end.render("Congratulations! ", 1,(255,0,0)) 
            end_text_second_line = font_end.render("You collected maximum points! ", 1,(255,0,0)) 
            screen.blit(end_text_first_line, (500 , 350))
            screen.blit(end_text_second_line, (430 , 380)) 
            screen.blit(scoretext, (10 , 4)) 
            pygame.display.update() 
            pygame.time.delay(2000)        
            pygame.event.wait()            
            menu_game()
        if player.lives == 0:                   #Ако играча е загубил всичките си животи, изведи съобщение и се върни в началното меню
            font_end = pygame.font.Font('files/Fonts/Adventure Subtitles.ttf',30)
            end_text_first_line = font_end.render("Game Over! ", 1,(255,0,0)) 
            end_text_second_line = font_end.render("You died!", 1,(255,0,0)) 
            screen.blit(end_text_first_line, (500 , 350))
            screen.blit(end_text_second_line, (515 , 380))
            pygame.display.update()  
            pygame.time.delay(2000)        
            pygame.event.wait()            
            menu_game()

        pygame.display.update()    

     
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

def about():                #Страница About
    pygame.init()
    screen = pygame.display.set_mode((1300,650), pygame.FULLSCREEN)
    background = pygame.image.load("files/fon_martinchovci.png")
    background = pygame.transform.scale(background, (1450,805))
    screen.blit(background, (-80, -100))
    font = pygame.font.Font('files/Fonts/Play-Regular.ttf',30)
    font_title=pygame.font.Font('files/Fonts/Adventure Subtitles.ttf',40)
    autors = font_title.render("ABOUT THE CREATOR:", 1,(145,183,220))
    Plamen1 = font.render("Plamen Dikov", 1, (145, 183, 220))
    Plamen2 = font.render("Specialty SIT, 1 Group ", 1, (145, 183, 220))
    Plamen3 = font.render("Fac No: 61362110 ", 1, (145, 183, 220))  
    Plamen_image = pygame.image.load("files/Skins/glaven.png")
    Plamen_image = pygame.transform.scale(Plamen_image, (187,250))
    while 1:
        screen.blit(Plamen1, (205, 400))
        screen.blit(Plamen2, (205, 430))
        screen.blit(Plamen3, (205, 460))
        screen.blit(autors, (205, 105))
        screen.blit(Plamen_image, (205, 155))
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                menu_game()
        pygame.display.update()

def help():             #Страница Help
    pygame.init()
    screen = pygame.display.set_mode((1300,650), pygame.FULLSCREEN)
    background = pygame.image.load("files/fon_martinchovci.png")
    background = pygame.transform.scale(background, (1450,805))
    screen.blit(background, (-80, -100))
    font_title=pygame.font.Font('files/Fonts/Adventure Subtitles.ttf',40)
    help = font_title.render("HOW TO PLAY:", 1,(145,183,220))  
    help_image = pygame.image.load("files/help.png") 
    help_image = pygame.transform.scale(help_image, (873,490))
    while 1:
        screen.blit(help, (205, 105))
        screen.blit(help_image, (205, 155))
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                menu_game()
        pygame.display.update()
        




def menu_game():                #Функция, извеждаща менюто
    import sys, pygame
    from pygame.locals import *
    import pygame.mixer
    pygame.mixer.init(44100, -16,2,2048) #Инициализация на миксера

#Промяна на иконата на прозореца
    icon = pygame.image.load("files/Skins/Martincho.png")
    icon = pygame.transform.scale(icon, (32, 32))
    pygame.display.set_icon(icon)

    pygame.mouse.set_visible(0)
#В заглавната лента се извежда името на играта 
    pygame.display.set_caption("RBP_V1.2")

#Избор на размер на прозореца 
    screen = pygame.display.set_mode((1300,650), pygame.FULLSCREEN) 

#Зареждане на фон на менюто
    background = pygame.image.load("files/Martinchovcite_menu1.png")
    background = pygame.transform.scale(background, (1450,805))
    screen.blit(background, (-80, -100))

#Пояснителен текст над менюто  
    font=pygame.font.Font('files/Fonts/Adventure Subtitles.ttf',30)
    menutext=font.render("MENU", 1,(145,183,220))
    screen.blit(menutext, (677, 230))

    menu = Menu()   #Инициализация на менюто

#Задаване на цветовете на фона, маркера и текста на менюто 
    menu.set_colors((145,183,220),(36,36,168),(59,60,189))

#Задаване на размер на менюто 
    menu.set_fontsize(30)

#Задаване на позиция, където менюто ще бъде изведено     
    menu.move_menu(75, 58)

#Задаване на съдържанието 
    menu.init(['Start','Help','About','Quit'], screen)
#Изчертаване на менюто 
    menu.draw()
    pygame.key.set_repeat(199,69)
    
    pygame.display.update()
    sound = pygame.mixer.Sound('files/Sounds/menu.wav') #Задаване на музика
    sound.set_volume(0.05)                              #Задаване на сила на звука
    while 1:
        
        sound.play()                                    #Изпълнение на музиката
        for event in pygame.event.get():                #Проверка коя от опциите е избрана и изпълнение на съответната функция
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    menu.draw(-1)
                if event.key == K_DOWN:
                    menu.draw(1)
                if event.key == K_RETURN:
                    if menu.get_position() == 0:
                        sound.stop()                        
                        game('Level_01.txt')
                    if menu.get_position() == 1:
                        sound.stop()                        
                        help()
                    if menu.get_position() == 2:
                        sound.stop()                                                
                        about()
                    if menu.get_position() == 3:
                        pygame.display.quit()
                        sys.exit()    
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
