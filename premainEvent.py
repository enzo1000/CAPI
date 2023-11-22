import pygame
import os
import numpy as np
from pygame.locals import *

from event import Event


class PremainEvent(Event):
	"""

	"""

	def __init__(self):
		Event.__init__(self)

		self.setName = False
		self.setBacklog = False
		self.setMode = False
		self.param = self.extractParam()

	def event(self, game):

		select = None

		while game.premainOn:

			for event in pygame.event.get():

				if event.type == MOUSEMOTION:
					select = self.findSelection(event.pos[0], event.pos[1])

				if event.type == MOUSEBUTTONDOWN:
					if select == 'npnb' : print('SET NB PLAYER')
					if select == 'npsn' : self.setName = True    ; select = None
					if select == 'blsn' : self.setBacklog = True ; select = None
					if select == 'mdch' : self.setMode = True    ; select = None
					if select == 'lg'   : game.premainOn, game.mainOn = False, True ; self.saveParam()

				if event.type == KEYDOWN:
					if event.key == K_ESCAPE : game.premainOn, game.menuOn = False, True

				if event.type == QUIT:
					game.gameOn, game.premainOn = False, False

			self.blitage(game.ds, select)

			if self.setMode : self.pre_main_set_mode_event(game.ds)
			if self.setBacklog : self.pre_main_set_backlog_event(game.ds)

	def findSelection(self, x, y):
		if self.inBox(x, y, self.imp.data.PMnpnb_Box) : return 'npnb'
		if self.inBox(x, y, self.imp.data.PMnpsn_Box) : return 'npsn'
		if self.inBox(x, y, self.imp.data.PMblsn_Box) : return 'blsn'
		if self.inBox(x, y, self.imp.data.PMmdch_Box) : return 'mdch'
		if self.inBox(x, y, self.imp.data.PMlg_Box) : return 'lg'


	def blitage(self, display, select):
		npColors   = self.imp.data.defaultColors.copy()
		npnbColors = self.imp.data.defaultColors.copy()
		npsnColors = self.imp.data.defaultColors.copy()
		blColors   = self.imp.data.defaultColors.copy()
		blsnColors = self.imp.data.defaultColors.copy()
		mdColors   = self.imp.data.defaultColors.copy()
		mdchColors = self.imp.data.defaultColors.copy()
		lgColors   = self.imp.data.defaultColors.copy()

		if select == 'npnb' : npnbColors[0] = self.imp.data.activColor
		if select == 'npsn' : npsnColors[0] = self.imp.data.activColor
		if select == 'blsn' : blsnColors[0] = self.imp.data.activColor
		if select == 'mdch' : mdchColors[0] = self.imp.data.activColor
		if select == 'lg'   : lgColors[0]   = self.imp.data.activColor

		display.blit(self.imp.image.back_main, (0, 0))
		self.labelisation(display, self.imp.font.menu_title, "Paramètre", (222, 222, 222), (0, 0), (1600, 100))

		self.blitTextBox(display, self.imp.data.PMnp_Box,   npColors,   'Nombre Player :', self.imp.font.menu_choice)
		self.blitTextBox(display, self.imp.data.PMnpnb_Box, npnbColors, str(self.param['nb_name']), self.imp.font.menu_choice)
		self.blitTextBox(display, self.imp.data.PMnpsn_Box, npsnColors, 'Set name', self.imp.font.menu_choice)

		self.blitTextBox(display, self.imp.data.PMbl_Box,   blColors,   'Choix BackLog :', self.imp.font.menu_choice)
		self.blitTextBox(display, self.imp.data.PMblsn_Box, blsnColors, self.imp.data.listBacklog[self.param['backlog']], self.imp.font.menu_choice)

		self.blitTextBox(display, self.imp.data.PMmd_Box,   mdColors,   'Choix Mode :', self.imp.font.menu_choice)
		self.blitTextBox(display, self.imp.data.PMmdch_Box, mdchColors, self.imp.data.listMode[self.param['mode']], self.imp.font.menu_choice)

		self.blitTextBox(display, self.imp.data.PMlg_Box,   lgColors,   'Lezgo !', self.imp.font.menu_choice)

		self.blitFPS(display)
		pygame.display.flip()


	def pre_main_set_mode_event(self, display):

		select = None

		while self.setMode:

			for event in pygame.event.get():

				if event.type == MOUSEMOTION:
					select = None
					for i, box in enumerate(self.imp.data.PMSMlist_Box):
						if self.inBox(event.pos[0], event.pos[1], box) : select = i

				if event.type == MOUSEBUTTONDOWN:
					if select is not None : 
						self.setMode = False
						self.param['mode'] = select
						return None

				if event.type == KEYDOWN:
					if event.key == K_ESCAPE : self.setMode = False

				if event.type == QUIT:
					game.gameOn, game.premainOn, self.setMode = False, False, False

			display.blit(self.imp.image.back_main, (0, 0))
			self.labelisation(display, self.imp.font.menu_title, "Choix Mode", (222, 222, 222), (0, 0), (1600, 100))

			self.blitTextBox(display, 
				self.imp.data.PMSMback_Box,
				((64, 0, 0), (128, 128, 128)),
				'Placeholder SetMode',
				self.imp.font.placeholder)

			for i, mode in enumerate(self.imp.data.listMode):
				colors = self.imp.data.defaultColors.copy()
				if i == select : colors[0] = self.imp.data.activColor

				self.blitTextBox(display, 
					self.imp.data.PMSMlist_Box[i],
					colors,
					mode,
					self.imp.font.menu_choice)

			self.blitFPS(display)
			pygame.display.flip()

	def pre_main_set_backlog_event(self, display):

		select = None

		while self.setBacklog:

			for event in pygame.event.get():

				if event.type == MOUSEMOTION:
					select = None
					for i, box in enumerate(self.imp.data.PMSBlist_Box):
						if self.inBox(event.pos[0], event.pos[1], box) : select = i

				if event.type == MOUSEBUTTONDOWN:
					if select is not None : 
						self.setBacklog = False
						self.param['backlog'] = select
						return None

				if event.type == KEYDOWN:
					if event.key == K_ESCAPE : self.setBacklog = False

				if event.type == QUIT:
					game.gameOn, game.premainOn, self.setBacklog = False, False, False

			display.blit(self.imp.image.back_main, (0, 0))
			self.labelisation(display, self.imp.font.menu_title, "Choix Backlog", (222, 222, 222), (0, 0), (1600, 100))

			self.blitTextBox(display, 
				self.imp.data.PMSBback_Box,
				((64, 0, 0), (128, 128, 128)),
				'Placeholder SetBacklog',
				self.imp.font.placeholder)

			for i, mode in enumerate(self.imp.data.listBacklog):
				colors = self.imp.data.defaultColors.copy()
				if i == select : colors[0] = self.imp.data.activColor

				score = f"{self.imp.data.testBacklog[mode][1][0]}/{self.imp.data.testBacklog[mode][1][2]}"

				self.blitTextBox(display, 
					self.imp.data.PMSBlist_Box[i],
					colors,
					mode,
					self.imp.font.menu_choice)

				self.blitTextBox(display, 
					self.imp.data.PMSBscor_Box[i],
					colors,
					score,
					self.imp.font.menu_choice)

			self.blitFPS(display)
			pygame.display.flip()