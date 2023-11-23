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

		self.testBacklog = read_json.findAllJson()
		self.listBacklog  = list(self.testBacklog.keys())
		self.PMSBlist_Box = [((500, 250 + 100*i), (490, 90)) for i in range(len(self.listBacklog))]
		self.PMSBscor_Box = [((1000, 250 + 100*i), (100, 90)) for i in range(len(self.listBacklog))]