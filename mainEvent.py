import pygame
import numpy as np
from pygame.locals import *

from event import Event
import import_json


class MainEvent(Event):
	"""
	Classe MainEvent hérité de Event
	Cette classe permet de gérer l'evenement principale de cette appli : jouons au planning poker
		-> Le jeu ce joue tache par tache, avec a chaque fois joueur par joueur
		-> On enregistrera le backlog a la fin (ou si on fait cafe !)
	"""

	def __init__(self):
		Event.__init__(self)
		self.lastCarte = -1

	def event(self, game):
		"""
		Methode qui lance le planning poker
		"""

		# On initialise les cartes
		self.activCartes = np.zeros(12).astype(int)
		# On extrait les paramètres
		self.param = self.extractParam()

		# On extrait le backlog choisi pour le planning poker
		self.backlogName = game.listBacklog[self.param['backlog']]
		self.backlog     = game.testBacklog[self.backlogName][0]

		# On place dans listTask les taches qui ne sont pas encore fait
		self.listTask = []
		for task, value in self.backlog.items():
			if value == -1:
				self.listTask.append(task)

		# Pour le debug
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
					# Observation de la carte sous la souris
					self.motionInCartes(event.pos)

				if event.type == MOUSEBUTTONDOWN:
					# Prise en compte de la selection de la carte par le joueur
					self.selectCartes(game)

				if event.type == QUIT:
					game.gameOn, game.mainOn = False, False

			self.blitage(game.ds)


	def blitage(self, display):
		"""
		Methode qui permet de rafraichir le display et d'afficher la nouvelle frame 
		"""
		display.blit(self.imp.image.back_main, (0, 0))
		self.labelisation(display, self.imp.font.roboto54, "Main", (222, 222, 222), (0, 0), (1600, 100))
		self.labelisation(display, self.imp.font.arial32, "Task : " + self.listTask[self.currentTask], (200, 180, 180), (0, 100), (1600, 80))
		self.labelisation(display, self.imp.font.arial32, "Player : " + self.param['list_name'][self.currentPlayer], (180, 200, 200), (0, 180), (1600, 80))

		# Affiche les cartes
		for i, (x, y, activ, carte) in enumerate(zip(self.imp.data.xCartes, self.imp.data.yCartes, self.activCartes, self.imp.image.cartes)):
			display.blit(carte, (x + activ*self.imp.data.dxActiv, y + activ*self.imp.data.dyActiv))

		self.blitFPS(display)
		pygame.display.flip()


	def motionInCartes(self, mouse):
		"""
		Methode qui regarde la cartes qui est sous la souris
		"""
		for i, (x, y) in enumerate(zip(self.imp.data.xCartes, self.imp.data.yCartes)):
			if x < mouse[0] < x + int(self.imp.data.dimCartes[0]/2) and y < mouse[1] < y + self.imp.data.dimCartes[1]:
				self.activCartes[i] = 1
				if self.lastCarte != i:
					self.imp.sound.carte.play()
				self.lastCarte = i
			else:
				self.activCartes[i] = 0


	def selectCartes(self, game):
		"""
		Methode qui selectionne la carte du joueur en cours
		"""
		select = None

		if sum(self.activCartes) == 1:
			select = self.imp.image.labelCartes[np.where(self.activCartes == 1)[0][0]]

			print(f"TOUR {self.loop} : Player {self.param['list_name'][self.currentPlayer]} vote {select} pour la task {self.listTask[self.currentTask]}")
			try:
				self.playerVote.append(int(select))
			except ValueError:
				if select == 'cafe':
					print('cafe')
				elif select == 'intero':
					print('intero')
				
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

				else:	#TODO Pourquoi pas un elif ?
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
		"""
		Methode utiliser par selecCartes pour changer de tache quand une est finis
		"""

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