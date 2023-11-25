import pygame
from pygame.locals import *
import import_json

class GameClass():

	def __init__(self, displayXY, displayCaption):
		pygame.init()

		self.ds = pygame.display.set_mode(displayXY)
		pygame.display.set_caption(displayCaption)

		self.gameOn    = True

		self.menuOn    = False
		self.premainOn = False
		self.mainOn    = False

	def loadBacklog(self, event):

		self.testBacklog = import_json.findAllJson()
		self.listBacklog  = list(self.testBacklog.keys())
		n = len(list(self.testBacklog.keys()))

		self.listBack = {'images' : event.imp.image.sprit_480_80,
			'imgBox': [((556, 250+100*i), (546, 248+100*i)) for i in range(n)],
			'text'  : list(self.testBacklog.keys()),
			'color' : event.imp.color.noir,
			'font'  : event.imp.font.font_roboto32,
			'box'   : [((560, 250 + 100*i), (480, 80)) for i in range(n)]}