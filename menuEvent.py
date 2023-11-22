import pygame
import numpy as np
from pygame.locals import *

from event import Event


class MenuEvent(Event):
	"""

	"""

	def __init__(self):
		Event.__init__(self)


	def event(self, game):

		select = None

		while game.menuOn:

			for event in pygame.event.get():

				if event.type == MOUSEMOTION:
					select = self.findSelection(event.pos[0], event.pos[1])

				if event.type == MOUSEBUTTONDOWN:
					if select == 'begin' : game.menuOn, game.premainOn = False, True
					if select == 'lang'  : print('Langue Event Not Make')
					if select == 'quit'  : game.gameOn, game.menuOn = False, False

				if event.type == KEYDOWN:
					if event.key == K_ESCAPE : game.gameOn, game.menuOn = False, False

				if event.type == QUIT:
					game.gameOn, game.menuOn = False, False

			self.blitage(game.ds, select)


	def findSelection(self, x, y):
		if self.inBox(x, y, self.imp.data.Mbg_Box) : return 'begin'
		if self.inBox(x, y, self.imp.data.Mlg_Box) : return 'lang'
		if self.inBox(x, y, self.imp.data.Mqt_Box) : return 'quit'


	def blitage(self, display, select):
		beginColors = self.imp.data.defaultColors.copy()
		langColors  = self.imp.data.defaultColors.copy()
		quitColors  = self.imp.data.defaultColors.copy()

		if select == 'begin' : beginColors[0] = self.imp.data.activColor
		if select == 'lang'  : langColors[0]  = self.imp.data.activColor
		if select == 'quit'  : quitColors[0]  = self.imp.data.activColor

		display.blit(self.imp.image.back_main, (0, 0))
		self.labelisation(display, self.imp.font.menu_title, "Menu", (222, 222, 222), (0, 0), (1600, 100))

		self.blitTextBox(display, 
			self.imp.data.Mbg_Box,
			beginColors,
			'Commencer !',
			self.imp.font.menu_choice)

		self.blitTextBox(display, 
			self.imp.data.Mlg_Box, 
			langColors,
			'Langue...?',
			self.imp.font.menu_choice)

		self.blitTextBox(display, 
			self.imp.data.Mqt_Box, 
			quitColors,
			'Quitter ...!',
			self.imp.font.menu_choice)

		self.blitFPS(display)
		pygame.display.flip()