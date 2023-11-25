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
		self.setNbPlayer = False
		self.param = self.extractParam()
		self.resetSelect()

	def event(self, game):

		game.loadBacklog(self)

		while game.premainOn:

			for event in pygame.event.get():

				if event.type == MOUSEMOTION:
					self.findSelection(event.pos[0], event.pos[1])

				if event.type == MOUSEBUTTONDOWN:
					if self.select['nbPlayer']   : self.setNbPlayer = True
					if self.select['setName']    : self.setName = True
					if self.select['setBacklog'] : self.setBacklog = True
					if self.select['setMode']    : self.setMode = True
					if self.select['lezgo']      : game.premainOn, game.mainOn = False, True ; self.saveParam(game)

				if event.type == KEYDOWN:
					if event.key == K_ESCAPE : game.premainOn, game.menuOn = False, True

				if event.type == QUIT:
					game.gameOn, game.premainOn = False, False

			self.blitage(game)

			if self.setNbPlayer : self.setNbPlayerEvent(game)
			if self.setName     : self.setNameEvent(game)
			if self.setMode     : self.setModeEvent(game)
			if self.setBacklog  : self.setBacklogEvent(game)

	def findSelection(self, x, y):
		if   self.inBox(x, y, self.imp.data.nbPlayer['box'])   : self.select['nbPlayer'] = 1 
		elif self.inBox(x, y, self.imp.data.setName['box'])    : self.select['setName'] = 1
		elif self.inBox(x, y, self.imp.data.setBacklog['box']) : self.select['setBacklog'] = 1
		elif self.inBox(x, y, self.imp.data.setMode['box'])    : self.select['setMode'] = 1
		elif self.inBox(x, y, self.imp.data.lezgo['box'])      : self.select['lezgo'] = 1
		else : self.resetSelect()

	def resetSelect(self):
		self.select = {
			'player' : 0,
			'nbPlayer' : 0,
			'setName' : 0,
			'backlog' : 0,
			'setBacklog' : 0,
			'mode' : 0,
			'setMode' : 0,
			'lezgo' : 0}

	def blitage(self, game):

		game.ds.blit(self.imp.image.back_main, (0, 0))
		self.labelisation(game.ds, self.imp.font.menu_title, "Paramètre", (222, 222, 222), (0, 0), (1600, 100))

		self.blitBox(game.ds, self.imp.data.player,   self.select['player'])
		self.blitBox(game.ds, self.imp.data.nbPlayer, self.select['nbPlayer'], text=str(self.param['nb_name']))
		self.blitBox(game.ds, self.imp.data.setName,  self.select['setName'])

		self.blitBox(game.ds, self.imp.data.backlog,    self.select['backlog'])
		self.blitBox(game.ds, self.imp.data.setBacklog, self.select['setBacklog'], text=game.listBacklog[self.param['backlog']])

		self.blitBox(game.ds, self.imp.data.mode,    self.select['mode'])
		self.blitBox(game.ds, self.imp.data.setMode, self.select['setMode'], text=self.imp.data.listMode['text'][self.param['mode']])

		self.blitBox(game.ds, self.imp.data.lezgo, self.select['lezgo'])

		self.blitFPS(game.ds)
		pygame.display.flip()

	def setNbPlayerEvent(self, game):

		self.param['nb_name'] = str(self.param['nb_name'])

		while self.setNbPlayer:

			for event in pygame.event.get():

				if event.type == KEYDOWN:

					if event.key == K_ESCAPE : self.setNbPlayer = False

					elif event.key in self.imp.data.keyValNUM.keys():
						if self.param['nb_name'] == '0' : self.param['nb_name'] = ''
						self.param['nb_name'] = str(self.param['nb_name']) + self.imp.data.keyValNUM[event.key]

					elif event.key == K_BACKSPACE:
						self.param['nb_name'] = str(self.param['nb_name'])[:-1]
						if len(self.param['nb_name']) == 0 : self.param['nb_name'] = '0'

					elif event.key == K_RETURN:
						self.param['nb_name'] = min(int(self.param['nb_name']), self.imp.data.maxPlayer)
						self.param['nb_name'] = max(int(self.param['nb_name']), self.imp.data.minPlayer)
						self.setNbPlayer = False

				if event.type == QUIT:
					game.gameOn, game.premainOn, setNbPlayer = False, False, False

			self.blitage(game)


	def setNameEvent(self, game):

		select = None

		niq = [0]*self.param['nb_name'] + [2]*(10-self.param['nb_name'])

		while self.setName:

			for event in pygame.event.get():

				if event.type == MOUSEMOTION:
					select = None
					for i, box in enumerate(self.imp.data.listName['box']):
						if self.inBox(event.pos[0], event.pos[1], box) : select = i

				if event.type == MOUSEBUTTONDOWN:
					pass

				if event.type == KEYDOWN:
					if event.key == K_ESCAPE : self.setName = False

				if event.type == QUIT:
					game.gameOn, game.premainOn, self.setName = False, False, False

			game.ds.blit(self.imp.image.back_main, (0, 0))
			self.labelisation(game.ds, self.imp.font.menu_title, "Choix Nom des joueurs", (222, 222, 222), (0, 0), (1600, 100))

			for i in range(10):
				activ = (i == select) * 1
				game.ds.blit(self.imp.data.listName['images'][activ + niq[i]], self.imp.data.listName['imgBox'][i][activ + niq[i]])
				self.labelisation(game.ds, 
					self.imp.data.listName['font'],
					self.param['list_name'][i], 
					self.imp.data.listName['color'],
					self.imp.data.listName['box'][i][0], self.imp.data.listName['box'][i][1], position='center')

			self.blitFPS(game.ds)
			pygame.display.flip()


	def setModeEvent(self, game):

		select = None

		while self.setMode:

			for event in pygame.event.get():

				if event.type == MOUSEMOTION:
					select = None
					for i, box in enumerate(self.imp.data.listMode['box']):
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

			game.ds.blit(self.imp.image.back_main, (0, 0))
			self.labelisation(game.ds, self.imp.font.menu_title, "Choix Mode", (222, 222, 222), (0, 0), (1600, 100))

			for i, mode in enumerate(self.imp.data.listMode['text']):
				activ = (i == select) * 1
				game.ds.blit(self.imp.data.listMode['images'][activ], self.imp.data.listMode['imgBox'][i][activ])
				self.labelisation(game.ds, 
					self.imp.data.listMode['font'],
					self.imp.data.listMode['text'][i], 
					self.imp.data.listMode['color'],
					self.imp.data.listMode['box'][i][0], self.imp.data.listMode['box'][i][1])

			self.blitFPS(game.ds)
			pygame.display.flip()

	def setBacklogEvent(self, game):

		select = None

		while self.setBacklog:

			for event in pygame.event.get():

				if event.type == MOUSEMOTION:
					select = None
					for i, box in enumerate(game.listBack['box']):
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

			game.ds.blit(self.imp.image.back_main, (0, 0))
			self.labelisation(game.ds, self.imp.font.menu_title, "Choix Backlog", (222, 222, 222), (0, 0), (1600, 100))

			for i, backlog in enumerate(game.listBacklog):
				activ = (i == select) * 1
				score = f"{game.testBacklog[backlog][1][1]}/{game.testBacklog[backlog][1][2]}"
				textBL = f"  [{score}] {backlog}"
				game.ds.blit(game.listBack['images'][activ], game.listBack['imgBox'][i][activ])
				self.labelisation(game.ds, 
					game.listBack['font'],
					textBL, 
					game.listBack['color'],
					game.listBack['box'][i][0], game.listBack['box'][i][1], position='left')

			self.blitFPS(game.ds)
			pygame.display.flip()