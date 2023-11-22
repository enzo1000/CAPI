import pygame
from pygame.locals import *

class GameClass():

	def __init__(self, displayXY, displayCaption):
		pygame.init()

		self.ds = pygame.display.set_mode(displayXY)
		pygame.display.set_caption(displayCaption)

		self.gameOn    = True

		self.menuOn    = False
		self.premainOn = False
		self.mainOn    = False