import pygame
import numpy as np
from pygame.locals import *

from event import Event
import import_json


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
					self.selectCartes(game)

				if event.type == QUIT:
					game.gameOn, game.mainOn = False, False

			self.blitage(game.ds)


	def blitage(self, display):
		display.blit(self.imp.image.back_main, (0, 0))
		self.labelisation(display, self.imp.font.roboto54, "Main", (222, 222, 222), (0, 0), (1600, 100))
		self.labelisation(display, self.imp.font.arial32, "Task : " + self.listTask[self.currentTask], (200, 180, 180), (0, 100), (1600, 80))
		self.labelisation(display, self.imp.font.arial32, "Player : " + self.param['list_name'][self.currentPlayer], (180, 200, 200), (0, 180), (1600, 80))

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

				print(f"\nFin du tour : {self.loop} | vote : {self.playerVote}")

				if self.loop == 0 or self.param['mode'] == 0: # Premier tour ou MODE Unanimité
					if len(set(self.playerVote)) == 1:
						print(f"Tout le monde est d'accord pour la tache {self.listTask[self.currentTask]}")
						self.backlog[self.listTask[self.currentTask]] = self.playerVote[0]

						self.nextTask(game)

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
						self.nextTask(game)

					if self.param['mode'] == 2: # MODE Mediane
						val = np.median(self.playerVote)
						print(f"Methode Med : {val} [{self.listTask[self.currentTask]}]")
						self.backlog[self.listTask[self.currentTask]] = val
						self.nextTask(game)

					if self.param['mode'] >= 3: # MODE Majo Abs. & Rela
						voteDiff  = list(set(self.playerVote))                         # valeur de vote distinctes
						countVote = [self.playerVote.count(vote) for vote in voteDiff] # countage du nombre de vote par valeur

						maxVote = max(countVote)            # nombre de vote de(s) valeur(s) les plus voter
						nbmaxVal = countVote.count(maxVote) # nombre de valeur de vote demander maxVote fois

						print('majo : ', voteDiff, countVote, maxVote, nbmaxVal)


						if self.param['mode'] == 3 and maxVote > self.param['nb_name']/2: # MODE Majo Abs.
							val = voteDiff[countVote.index(maxVote)]
							print(f"Methode Maj Abs : {val} [{self.listTask[self.currentTask]}]")
							self.backlog[self.listTask[self.currentTask]] = val
							self.nextTask(game)

						elif self.param['mode'] == 4 and nbmaxVal == 1:                   # MODE Majo Rela
							val = voteDiff[countVote.index(maxVote)]
							print(f"Methode Maj rela : {val} [{self.listTask[self.currentTask]}]")
							self.backlog[self.listTask[self.currentTask]] = val
							self.nextTask(game)

						else:
							print(f"Tout le monde n'est pas d'accord pour la tache {self.listTask[self.currentTask]}")
							self.loop += 1
							self.currentPlayer = 0
							self.playerVote = []

			
	def nextTask(self, game):

		if self.currentTask + 1 == self.totalTask:
			print('C fini !')
			print(self.backlog)
			self.currentPlayer = 0
			game.mainOn, game.menuOn = False, True
			import_json.writeJson(self.backlogName, self.backlog)
		else:
			self.currentTask += 1
			self.currentPlayer = 0
			self.playerVote = []