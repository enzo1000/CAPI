import pygame
import numpy as np
from pygame.locals import *

from event import Event


class MainEvent(Event):
	"""

	"""

	def __init__(self):
		Event.__init__(self)

	def event(self, game):

		self.activCartes = np.zeros(12).astype(int)
		self.param = self.extractParam()

		self.backlogName = game.listBacklog[self.param['backlog']]
		self.backlog     = game.testBacklog[self.backlogName][0]

		self.listTask = []

		for task, value in self.backlog.items():
			if value == -1:
				self.listTask.append(task)

		print(self.backlogName, ' : ', self.backlog, ' | ', self.listTask)

		self.totalTask = len(self.listTask)

		self.playerVote = []
		self.loop = 0
		self.currentTask = 0
		self.currentPlayer = 0

		while game.mainOn:

			for event in pygame.event.get():
				if event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						game.mainOn, game.menuOn = False, True

				if event.type == MOUSEMOTION:
					self.motionInCartes(event.pos)

				if event.type == MOUSEBUTTONDOWN:
					select = self.selectCartes(game)

				if event.type == QUIT:
					game.gameOn, game.mainOn = False, False

			#J'ai add ça, atm ça sert à rien : Enzo
			if len(game.listBacklog) >= 1:
				self.blitage(game.ds)

	def blitage(self, display):
		display.blit(self.imp.image.back_main, (0, 0))
		self.labelisation(display, self.imp.font.menu_title, "Main", (222, 222, 222), (0, 0), (1600, 100))
		self.labelisation(display, self.imp.font.task, "Task : " + self.listTask[self.currentTask], (180, 0, 0), (0, 100), (1600, 80))
		self.labelisation(display, self.imp.font.player, "Player : " + self.param['list_name'][self.currentPlayer], (120, 0, 0), (0, 180), (1600, 80))

		#BLIT CARTES :
		for i, (x, y, activ, carte) in enumerate(zip(self.imp.data.xCartes, self.imp.data.yCartes, self.activCartes, self.imp.image.cartes)):
			display.blit(carte, (x + activ*self.imp.data.dxActiv, y + activ*self.imp.data.dyActiv))

		self.blitFPS(display)
		pygame.display.flip()

	def motionInCartes(self, mouse):
		for i, (x, y) in enumerate(zip(self.imp.data.xCartes, self.imp.data.yCartes)):
			if x < mouse[0] < x + int(self.imp.data.dimCartes[0]/2) and y < mouse[1] < y + self.imp.data.dimCartes[1]:
				self.activCartes[i] = 1
			else:
				self.activCartes[i] = 0


	def selectCartes(self, game):
		select = None
		if sum(self.activCartes) == 1:
			select = self.imp.image.labelCartes[np.where(self.activCartes == 1)[0][0]]

			print(f"TOUR {self.loop} : Player {self.param['list_name'][self.currentPlayer]} vote {select} pour la task {self.listTask[self.currentTask]}")

			self.playerVote.append(int(select))
			self.currentPlayer += 1

			if self.currentPlayer == self.param['nb_name']:

				print(f"Fin du tour : {self.loop} | vote : {self.playerVote}")

				if self.loop == 0 or self.param['mode'] == 0: # Premier tour ou MODE Unanimité
					if len(set(self.playerVote)) == 1:
						print(f"Tout le monde est d'accord pour la tache {self.listTask[self.currentTask]}")
						self.backlog[self.listTask[self.currentTask]] = self.playerVote[0]

						if self.currentTask + 1 == self.totalTask:
							print('C fini !')
							print(self.backlog)
							self.currentPlayer = 0
							game.mainOn, game.menuOn = False, True
						else:
							self.currentTask += 1
							self.currentPlayer = 0
							self.playerVote = []

					else:
						print(f"Tout le monde n'est pas d'accord pour la tache {self.listTask[self.currentTask]}")
						self.loop += 1
						self.currentPlayer = 0
						self.playerVote = []

				else:
					if self.param['mode'] == 1: # MODE Moyenne
						val = np.mean(self.playerVote)
						print(f"Methode Moy : {val} [{self.listTask[self.currentTask]}]")
						self.backlog[self.listTask[self.currentTask]] = val

					if self.param['mode'] == 2: # MODE Mediane
						val = np.median(self.playerVote)
						print(f"Methode Moy : {val} [{self.listTask[self.currentTask]}]")
						self.backlog[self.listTask[self.currentTask]] = val

					if self.param['mode'] == 3: # MODE Majo Abs.
						print('WARNING : Mode Majo. Abs. non fait encore')

					if self.param['mode'] == 4: # MODE Majo rela.
						print('WARNING : Mode Majo. Rela. non fait encore')

					if self.currentTask + 1 == self.totalTask:
						print('C fini !')
						print(self.backlog)
						self.currentPlayer = 0
						game.mainOn, game.menuOn = False, True
					else:
						self.loop = 0
						self.currentTask += 1
						self.currentPlayer = 0
						self.playerVote = []
			
		return select