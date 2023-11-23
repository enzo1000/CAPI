import pygame
import time
import os
import numpy as np
from pygame.locals import *
from class_import import importation




class Event():
	"""
		
	"""

	def __init__(self):
		self.time0       = time.time()
		self.timeRefresh = time.time()
		self.refreshFPS  = 0.5
		self.spf         = np.ones(20)
		self.fps         = '---'
		self.imp         = importation()


	def blitFPS(self, ds):

		self.spf[:-1], self.spf[-1] = self.spf[1:], time.time() - self.time0
		self.time0 = time.time()
		
		if time.time() - self.timeRefresh > self.refreshFPS:
			self.timeRefresh = time.time()
			self.fps = str(int(20 / np.sum(self.spf)))

		self.labelisation(ds, self.imp.font.fps, f"{self.fps:3} FPS", (222, 222, 222), (1600-64, 900-24), (64, 24))

	
	def labelisation(self, display, font, text, color, X, dX, position='center'):
		surface = font.render(text, True, color)
		if position == 'center' : rect = surface.get_rect(center  = (int(X[0] + dX[0]/2), int(X[1] + dX[1]/2)))
		if position == 'left'   : rect = surface.get_rect(midleft = (int(X[0])          , int(X[1] + dX[1]/2)))
		display.blit(surface, rect)


	def blitTextBox(self, display, Box, colors, text, font):

		surface_dessin = pygame.Surface(Box[1])
		surface_dessin.fill(colors[0])
		display.blit(surface_dessin, Box[0])
		self.labelisation(display, font, text, colors[1], Box[0], Box[1])


	def inBox(self, x, y, Box):

		if 0 < x - Box[0][0] < Box[1][0] and 0 < y - Box[0][1] < Box[1][1]:
			return True
		else:
			return False


	def extractParam(self, folder='data'):

		if True in ['param.ini' in file for file in os.listdir(f"./{folder}/")]:
			try:
				param = {}
				f = open(f"./{folder}/param.ini", 'r').read().replace(' ', '').split('\n')[1:]
				param['mode']    = int(f[0].split(':')[1].split('[')[0])
				param['backlog'] = int(f[1].split(':')[1].split('[')[0])
				param['nb_name'] = int(f[2].split(':')[1])
				param['list_name'] = []

				for i in range(param['nb_name']):
					param['list_name'].append(f[3+i].split(':')[1])
			except:
				param = {'mode' : 0, 'nb_name' : 2, 'backlog' : 0, 'list_name' : ['Player1', 'Player2']}
		else:
			param = {'mode' : 0, 'nb_name' : 2, 'backlog' : 0, 'list_name' : ['Player1', 'Player2']}

		return param


	def saveParam(self, game, folder='data'):

		f = open(f"./{folder}/param.ini", "w")
		f.write(f"Paramètre :\n")
		f.write(f"Mode          : {self.param['mode']} [{self.imp.data.listMode[self.param['mode']]}]\n")
		f.write(f"BackLog       : {self.param['backlog']} [{game.listBacklog[self.param['backlog']]}]\n")
		f.write(f"Player number : {self.param['nb_name']}\n")
		[f.write(f"- Player {i+1} : {name}\n") for i, name in enumerate(self.param['list_name'])]
		f.close()