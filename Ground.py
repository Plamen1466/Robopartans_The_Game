from Entity import Entity
import pygame 
from pygame.locals import *


class Ground(Entity):
	def __init__(self, x, y, image_path):
		Entity.__init__(self)
		self.image = pygame.image.load(image_path+"/ground.png")
		self.image = pygame.transform.scale(self.image, (64*6, 64))
		self.image.convert()

		self.rect = Rect(x, y, 64*6, 64)

	
