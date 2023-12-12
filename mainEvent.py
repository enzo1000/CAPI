import pygame
import numpy as np
from pygame.locals import *
from time import time

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

		self.endTaskEvent = EndTaskEvent()
		self.explicationEvent = ExplicationEvent()
		self.endMainEvent = EndMainEvent()

		self.endTask = False
		self.explication = False
		self.endMain = False

		self.lastCarte = -1
		self.currentChrono = time()
		self.thereIsExplication = False 

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

		self.somebobyWantACoffee = False

		self.totalTask = len(self.listTask)
		self.playerVote = []
		self.loop = 0
		self.currentTask = 0
		self.currentPlayer = 0
		self.currentChrono = time()

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

			if (self.param['time'] - time() + self.currentChrono) < 0 and self.param['cocheChrono'] == 1:
				self.selectCartes(game)

			self.blitage(game.ds)


	def strChrono(self, t):
		"""
		Methode permettant de retourner une formatage visuel plus correct du temps
		"""
		if self.param['cocheChrono'] : return f"{int(t//60):01}'{int(t%60):02}\""
		else : return f"-'--\""


	def blitageExplication(self, game, sentence):

		self.blitBox(game.ds, self.imp.data.explication, 0, text='')

		nbRetour = len(sentence)
		for i, texte in enumerate(sentence):

			Xi = list(self.imp.data.explication['box'][0])
			Xi[1] += i*self.imp.data.explicationFontSize - (nbRetour)*self.imp.data.explicationFontSize/2

			self.labelisation(game.ds, 
				self.imp.data.explication['font'],
				texte, 
				self.imp.data.explication['color'],
				Xi, self.imp.data.explication['box'][1], position='center')


	def blitage(self, display):
		"""
		Methode qui permet de rafraichir le display et d'afficher la nouvelle frame 
		"""
		display.blit(self.imp.image.back_main, (0, 0))
		self.labelisation(display, self.imp.font.roboto54, "Planning Poker", (222, 222, 222), (0, 0), (1600, 100))
		
		if self.param['cocheChrono'] == 1 : self.blitBox(display, self.imp.data.currentTime, text=self.strChrono(int(self.param['time'] - time() + self.currentChrono)))

		self.blitBox(display, self.imp.data.task)
		self.blitBox(display, self.imp.data.currentTask, text=f"  {self.listTask[self.currentTask]}", position='left')

		self.blitBox(display, self.imp.data.mainPlayer)
		self.blitBox(display, self.imp.data.currentMainPlayer, text=f"  {self.param['list_name'][self.currentPlayer]}", position='left')

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

		# On regarde si le joueur a cliquer sur une cartes ou si il a plus de temps pour repondre
		if sum(self.activCartes) == 1 or (self.param['time'] - time() + self.currentChrono) < 0 and self.param['cocheChrono'] == 1:

			# On selectionne 'interro' si le joueur n'a pas cliquer a temps
			if (self.param['time'] - time() + self.currentChrono) < 0 and self.param['cocheChrono'] == 1 : select = 'intero'
			else : select = self.imp.image.labelCartes[np.where(self.activCartes == 1)[0][0]]

			print(f"TOUR {self.loop} : Player {self.param['list_name'][self.currentPlayer]} vote {select} pour la task {self.listTask[self.currentTask]}")
			try:
				self.playerVote.append(int(select))
			except ValueError:
				if select == 'cafe':
					self.playerVote.append('CAFE')
				elif select == 'intero':
					self.playerVote.append('?')
				
			self.currentPlayer += 1

			# Tout les joueurs ont jouer 
			if self.currentPlayer == self.param['nb_name']:
				print(f"Fin du tour : {self.loop} | vote : {self.playerVote}")


				# On extrait les valeur contenu dans les votes :
				values = self.playerVote.copy()
				while '?' in values : values.pop(values.index('?'))
				while 'CAFE' in values : values.pop(values.index('CAFE'))


				# Un ou plusieurs joueurs on voté pour la pause !
				if 'CAFE' in self.playerVote: 
					print('On fait la pause salut...')

					self.playerCafe = []
					oldIndex = 0
					for _ in range(self.playerVote.count('CAFE')):
						curIndex = self.playerVote[oldIndex:].index('CAFE') + oldIndex
						self.playerCafe.append(self.param['list_name'][curIndex])
						oldIndex = curIndex + 1
					print(f"Joueur valeur Cafe : {self.playerCafe}")
					self.endMain = True
					self.endMainEvent.event(game, self, ending='cafe')

					self.currentPlayer = 0
					game.mainOn, game.menuOn = False, True
					import_json.writeJson(self.backlogName, self.backlog)


				# Premier tour ou MODE Unanimité
				elif self.loop == 0 or self.param['mode'] == 0:
					# Tout le monde a directement voter pareil 
					if len(set(values)) == 1:
						print(f"Tout le monde est d'accord pour la tache {self.listTask[self.currentTask]} : {values[0]}")
						self.backlog[self.listTask[self.currentTask]] = values[0]
						self.finalValue = values[0]
						self.nextTask(game)
					# Les joueurs ne sont pas tous d'accord
					else:
						self.explicationPlease(game, values)
						print('')


				# Deuxième tour et MODE différents de Unanimité
				else:
					if self.param['mode'] == 1: # MODE Moyenne
						self.finalValue = round(np.mean(values))
						print(f"Methode Moy : {self.finalValue} [{self.listTask[self.currentTask]}]")
						self.backlog[self.listTask[self.currentTask]] = self.finalValue
						self.nextTask(game)

					if self.param['mode'] == 2: # MODE Mediane
						self.finalValue = round(np.median(values))
						print(f"Methode Med : {self.finalValue} [{self.listTask[self.currentTask]}]")
						self.backlog[self.listTask[self.currentTask]] = self.finalValue
						self.nextTask(game)

					if self.param['mode'] >= 3: # MODE Majo Abs. & Rela
						voteDiff  = list(set(values))                                  # valeur de vote distinctes
						countVote = [self.playerVote.count(vote) for vote in voteDiff] # countage du nombre de vote par valeur

						maxVote = max(countVote)            # nombre de vote de(s) valeur(s) les plus voter
						nbmaxVal = countVote.count(maxVote) # nombre de valeur de vote demander maxVote fois

						print('majo : ', voteDiff, countVote, maxVote, nbmaxVal)

						if self.param['mode'] == 3 and maxVote > self.param['nb_name']/2: # MODE Majo Abs.
							self.finalValue = voteDiff[countVote.index(maxVote)]
							print(f"Methode Maj Abs : {self.finalValue} [{self.listTask[self.currentTask]}]")
							self.backlog[self.listTask[self.currentTask]] = self.finalValue
							self.nextTask(game)

						elif self.param['mode'] == 4 and nbmaxVal == 1:                   # MODE Majo Rela
							self.finalValue = voteDiff[countVote.index(maxVote)]
							print(f"Methode Maj rela : {self.finalValue} [{self.listTask[self.currentTask]}]")
							self.backlog[self.listTask[self.currentTask]] = self.finalValue
							self.nextTask(game)

						else:
							self.explicationPlease(game, values)
							print('')

			self.currentChrono = time()

			
	def nextTask(self, game):
		"""
		Methode utiliser par selecCartes pour changer de tache quand une est finis
		"""
		self.thereIsExplication = False
		self.nextBoxText = "Tache Suivante"
		self.endTask = True
		self.endTaskEvent.event(game, self)

		if self.currentTask + 1 == self.totalTask:
			print('C fini !')
			print(self.backlog)
			
			self.endMain = True
			self.endMainEvent.event(game, self, "ending")

			self.currentPlayer = 0
			game.mainOn, game.menuOn = False, True
			import_json.writeJson(self.backlogName, self.backlog)
		else:
			self.currentTask += 1
			self.loop = 0
			self.currentPlayer = 0
			self.playerVote = []
			print('')


	def explicationPlease(self, game, values):
		print(f"Tout le monde n'est pas d'accord pour la tache {self.listTask[self.currentTask]}")
		self.vmin = min(values)
		self.vmax = max(values)

		# Recuperation des players ayant voter l'extreme Minimum
		playerMin = []
		oldIndex = 0
		for _ in range(values.count(self.vmin)):
			curIndex = self.playerVote[oldIndex:].index(self.vmin) + oldIndex
			playerMin.append(self.param['list_name'][curIndex])
			oldIndex = curIndex + 1
		print(f"Joueur valeur min [{self.vmin}] : {playerMin}")

		# Recuperation des players ayant voter l'extreme Maximum
		playerMax = []
		oldIndex = 0
		for _ in range(values.count(self.vmax)):
			curIndex = self.playerVote[oldIndex:].index(self.vmax) + oldIndex
			playerMax.append(self.param['list_name'][curIndex])
			oldIndex = curIndex + 1
		print(f"Joueur valeur min [{self.vmax}] : {playerMax}")

		# On affiche les votes de tout le monde
		self.nextBoxText = "Explication !"
		self.endTaskEvent.event(game, self)


		# On demande aux extremes de s'expliquer
		self.listExplication = dict()
		for player in playerMin:
			self.explicationEvent.event(game, self, player, self.vmin)
		for player in playerMax:
			self.explicationEvent.event(game, self, player, self.vmax)

		# Presentation de toutes les explications :
		print(f"LISTES EXPLICATIONS :")
		for key, val in self.listExplication.items():
			print(f"Joueur {key:16} : {val}")

		self.thereIsExplication = True
		self.nextBoxText = "Prochain tour !"
		self.endTaskEvent.event(game, self)


		# On passe au prochain tour
		self.thereIsExplication = False
		self.loop += 1
		self.currentPlayer = 0
		self.playerVote = []




class EndTaskEvent(Event):
	"""
	Class utilisé par MainEvent pour presenter les votes 
	"""

	def __init__(self):
		Event.__init__(self)
		self.nextBox = 0

	def event(self, game, mainEvent):
		"""
		Methode qui affiche les votes de chacun avant de continuer 
		    -> Soit a la tache suivante
		    -> Soit aux explications
		"""
		self.nextBox = 0 # nextBox est soit la tache suivante "Ok" ou pour passer au explication "Explication"
		self.niq = [0]*mainEvent.param['nb_name'] + [2]*(self.imp.data.maxPlayer-mainEvent.param['nb_name'])
		mainEvent.endTask = True
		self.select = None

		while mainEvent.endTask:

			for event in pygame.event.get():

				if event.type == MOUSEMOTION:
					# Survol de nextBox
					self.nextBox = 0
					if self.inBox(event.pos[0], event.pos[1], self.imp.data.nextBox['box']) : 
						self.nextBox = 1	
					# Survol des votes
					self.select = None
					for i in range(mainEvent.param['nb_name']):
						if self.inBox(event.pos[0], event.pos[1], self.imp.data.listVotes['box'][i]) or self.inBox(event.pos[0], event.pos[1], self.imp.data.caseVotes['box'][i]):
							self.select = i

				if event.type == MOUSEBUTTONDOWN:
					if self.nextBox == 1: # Si on appuie sur nextBox
						mainEvent.endTask = False

				if event.type == KEYDOWN:
					if event.key == K_ESCAPE: 
						mainEvent.endTask = False

				if event.type == QUIT:
					game.gameOn, game.premainOn, mainEvent.endTask = False, False, False

			self.blitage(game, mainEvent)


	def blitage(self, game, mainEvent):
		"""
		Methode qui permet de rafraichir le display et d'afficher la nouvelle frame
		"""
		game.ds.blit(self.imp.image.back_main, (0, 0))
		self.labelisation(game.ds, self.imp.font.roboto54, f"Résumé : {mainEvent.listTask[mainEvent.currentTask]}", (222, 222, 222), (0, 0), (1600, 100))

		if mainEvent.nextBoxText == 'Tache Suivante':
			self.blitBox(game.ds, self.imp.data.finalValue, 0, text=f"{self.imp.data.listMode['text'][mainEvent.param['mode']]} :")
			self.blitBox(game.ds, self.imp.data.caseValue, 0, text=str(mainEvent.finalValue))

		for i in range(mainEvent.param['nb_name']):
			# Affiche les ,oms des players
			game.ds.blit(self.imp.data.listVotes['images'][0], self.imp.data.listVotes['imgBox'][i][0])
			self.labelisation(game.ds, 
				self.imp.data.listVotes['font'],
				f"  {mainEvent.param['list_name'][i]}",
				self.imp.data.listVotes['color'],
				self.imp.data.listVotes['box'][i][0], self.imp.data.listVotes['box'][i][1], position='left')

			# Permet de savoir si le player i a voter une valeur extreme
			if   mainEvent.nextBoxText != "Tache Suivante" and mainEvent.playerVote[i] == mainEvent.vmin : colorCase = 1
			elif mainEvent.nextBoxText != "Tache Suivante" and mainEvent.playerVote[i] == mainEvent.vmax : colorCase = 2
			elif mainEvent.playerVote[i] == '?' : colorCase = 3
			else : colorCase = 0

			# Affiche le votes des players
			game.ds.blit(self.imp.data.caseVotes['images'][colorCase], self.imp.data.caseVotes['imgBox'][i][0])
			self.labelisation(game.ds, 
				self.imp.data.caseVotes['font'],
				f"{mainEvent.playerVote[i]}",
				self.imp.data.caseVotes['color'],
				self.imp.data.caseVotes['box'][i][0], self.imp.data.caseVotes['box'][i][1], position='center')

		self.blitBox(game.ds, self.imp.data.nextBox, self.nextBox, text=mainEvent.nextBoxText)

		if mainEvent.thereIsExplication and self.select is not None and mainEvent.param['list_name'][self.select] in mainEvent.listExplication.keys():
			# self.blitBox(game.ds, self.imp.data.explication, 0, text=mainEvent.listExplication[mainEvent.param['list_name'][self.select]])
			mainEvent.blitageExplication(game, mainEvent.listExplication[mainEvent.param['list_name'][self.select]])

		self.blitFPS(game.ds)
		pygame.display.flip()		





class ExplicationEvent(Event):
	"""
	Class utilisé par MainEvent pour que les joueurs extremes s'explique (un par un)
	"""

	def __init__(self):
		Event.__init__(self)
		self.currentPlayer = '0x413$Ae'


	def event(self, game, mainEvent, currentPlayer, value):
		"""
		Methode qui affiche l'interface pour que les joueurs extremes s'explique (un par un)
		"""
		self.valider = 0 # bouton valider
		self.text = ''   # Contenu de l'explication
		self.allSentence = []
		self.currentPlayer = currentPlayer
		self.lshift = False
		mainEvent.explication = True

		while mainEvent.explication:

			for event in pygame.event.get():

				if event.type == MOUSEMOTION:
					self.valider = 0
					if self.inBox(event.pos[0], event.pos[1], self.imp.data.nextBox['box']) : self.valider = 1	# Survol nextBox

				if event.type == MOUSEBUTTONDOWN:
					if self.valider == 1: # Si on appuie sur nextBox
						mainEvent.explication = False

				if event.type == KEYDOWN:
					if event.key == K_ESCAPE: 
						mainEvent.explication = False

					# Ajout de la lettre si une touche du clavier est dans la liste des touche importer dans 'self.imp.data.keyVal'
					elif event.key in self.imp.data.keyValSPACE.keys() and len(self.text) < self.imp.data.limitExplication:
						if self.lshift: # Mettre la lettre en majuscule si LSHIFT en maintenue
							self.text += self.imp.data.keyValCAP_SPACE[event.key]
						else:           # Sinon, mettre la lettre en minuscule (par default)
							self.text += self.imp.data.keyValSPACE[event.key]

					# On prend en compte l'appuie sur LSHIFT pour mettre une lettre en majuscule
					elif event.key == K_LSHIFT:
						self.lshift = True

					# Efface le dernier caractère si on appuie sur BACKSPACE (c'est la touche effacer)
					elif event.key == K_BACKSPACE:
						if len(self.text) != 0: # Mais pas si c'est deja vide !
							self.text = self.text[:-1]

					elif event.key == K_RETURN or event.key == K_KP_ENTER:
						mainEvent.explication = False

					self.formatText()

				if event.type == KEYUP:
					if event.key == K_LSHIFT:
						self.lshift = False

				if event.type == QUIT:
					game.gameOn, game.premainOn, mainEvent.explication = False, False, False

			self.blitage(game, mainEvent)

		mainEvent.listExplication[currentPlayer] = self.allSentence


	def formatText(self):
		tokens = self.text.split(' ')
		num = -1
		allSentence = []

		while len(tokens) > 0:

			nowph = tokens.pop(0)
			num += 1

			while len(tokens) > 0 and len(nowph + tokens[0]) < self.imp.data.explicationRL:
				nowph += ' ' + tokens.pop(0)

			allSentence.append(nowph)

		self.allSentence = allSentence


	def blitage(self, game, mainEvent):
		"""
		Methode qui permet de rafraichir le display et d'afficher la nouvelle frame
		"""
		game.ds.blit(self.imp.image.back_main, (0, 0))
		self.labelisation(game.ds, self.imp.font.roboto54, f"Explication de {self.currentPlayer}", (222, 222, 222), (0, 0), (1600, 100))


		mainEvent.blitageExplication(game, self.allSentence)

		# nbRetour = len(self.allSentence)
		# for i, texte in enumerate(self.allSentence):

		# 	Xi = list(self.imp.data.explication['box'][0])
		# 	Xi[1] += i*self.imp.data.explicationFontSize - (nbRetour)*self.imp.data.explicationFontSize/2

		# 	self.labelisation(game.ds, 
		# 		self.imp.data.explication['font'],
		# 		texte, 
		# 		self.imp.data.explication['color'],
		# 		Xi, self.imp.data.explication['box'][1], position='center')

		self.blitBox(game.ds, self.imp.data.nextBox, self.valider, text='Envoyer !')
		self.blitFPS(game.ds)
		pygame.display.flip()





class EndMainEvent(Event):
	"""
	Class utiliser par la MainEvent pour enregistrer le backlog quand un joueur demande une pause
	"""

	def __init__(self):
		Event.__init__(self)


	def event(self, game, mainEvent, ending):
		"""
		Methode qui lance l'interface pour enregistrer le backlog quand un joueur demande une pause
		"""
		self.fin = 0
		self.formatText(mainEvent, ending)

		while mainEvent.endMain:

			for event in pygame.event.get():

				if event.type == MOUSEMOTION:
					self.fin = 0
					if self.inBox(event.pos[0], event.pos[1], self.imp.data.fin['box']) : self.fin = 1

				if event.type == MOUSEBUTTONDOWN:
					if self.fin == 1: 
						game.menuOn, game.mainOn, mainEvent.endMain = True, False, False
						return None

				if event.type == KEYDOWN:
					pass #PAS DESCAPE ICI :(((

				if event.type == QUIT:
					game.gameOn, game.mainOn, mainEvent.endMain = False, False, False

			self.blitage(game, mainEvent)


	def formatText(self, mainEvent, ending):

		if ending == 'cafe':
			if len(mainEvent.playerVote) == 1 : self.text = f"Le joueur {mainEvent.playerCafe[0]} demande une pause !"
			else : self.text = f"Les joueurs {', '.join(mainEvent.playerCafe[:-1])} et {mainEvent.playerCafe[-1]} demandent une pause !"
		if ending == 'ending':
			self.text = "Toutes les taches du Backlog sont finis !"

		tokens = self.text.split(' ')
		num = -1
		allSentence = []

		while len(tokens) > 0:

			nowph = tokens.pop(0)
			num += 1

			while len(tokens) > 0 and len(nowph + tokens[0]) < self.imp.data.explicationRL:
				nowph += ' ' + tokens.pop(0)

			allSentence.append(nowph)

		self.allSentence = allSentence


	def blitage(self, game, mainEvent):
		"""
		Methode qui permet de rafraichir le display et d'afficher la nouvelle frame
		"""
		game.ds.blit(self.imp.image.back_main, (0, 0))
		self.labelisation(game.ds, self.imp.font.roboto54, "C'est la pause !", (222, 222, 222), (0, 0), (1600, 100))

		mainEvent.blitageExplication(game, self.allSentence)

		self.blitBox(game.ds, self.imp.data.fin, self.fin)

		self.blitFPS(game.ds)
		pygame.display.flip()