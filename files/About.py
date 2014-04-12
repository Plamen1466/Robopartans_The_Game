import sys, pygame, pygame.mixer, time

from pygame.locals import *


pygame.init()
size = width, higth = 1200, 600
width = 110
height = 144
screen = pygame.display.set_mode(size)


font = pygame.font.Font('files/Fonts/Play-Regular.ttf',20)
font_title=pygame.font.Font('files/Fonts/Adventure Subtitles.ttf',30)

history_text1 = font.render("Robopartans: The Game is a project created for the course 'Teaching Practice' at the Technical University of Varna in 2014.", 1,(145,183,220))
history_text2 = font.render("The role of the main character is played by symbol Robopartans - Martincho. ", 1,(145,183,220)) 
info_RBP = font.render("More information about Robopartans and its activities can be found at: www.robopartans.com ", 1, (145, 183, 220))
autors = font_title.render("AUTORS:", 1,(145,183,220))
Plamen1 = font.render("Plamen Dikov", 1, (145, 183, 220))
Plamen2 = font.render("Specialty SIT, 1 Group ", 1, (145, 183, 220))
Plamen3 = font.render("Fac No: 61362110 ", 1, (145, 183, 220))
Mariya1 = font.render("Maria Yancheva", 1, (237, 136, 185))
Mariya2 = font.render("Specialty SIT, 1 Group ", 1, (237, 136, 185))
Mariya3 = font.render("Fac No: 61362107 ", 1, (237, 136, 185))

skin_Plamen = pygame.image.load("files/Skins/Martincho.png")
skin_Mimi = pygame.image.load("files/Skins/Martincho_rozov.png")
skin_Plamen = pygame.transform.scale(skin_Plamen, (width, height))
skin_Mimi = pygame.transform.scale(skin_Mimi, (width, height))

abouttext=font_title.render("ABOUT:", 1,(145,183,220))

screen.blit(skin_Plamen, (320,200))
screen.blit(skin_Mimi, (665,200))
while 1:
    screen.blit(abouttext, (5, 5))
    screen.blit(history_text1, (5, 40))
    screen.blit(history_text2, (5, 65))
    screen.blit(info_RBP, (5, 90))
    screen.blit(Plamen1, (305, 340))
    screen.blit(Plamen2, (305, 365))
    screen.blit(Plamen3, (305, 390))
    screen.blit(Mariya1, (650, 340))
    screen.blit(Mariya2, (650, 365))
    screen.blit(Mariya3, (650, 390))
    screen.blit(autors, (475, 155))
    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
    pygame.display.update()
    
