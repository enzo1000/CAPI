import pygame
import os
import numpy as np
from pygame.locals import *

from event import Event
import import_json


class PremainEvent(Event):
	"""
	Classe premainEvent hérité de Event
	Cette classe permet de gérer les paramètre voulu avant de lancer une partie de planning poker. 
	Elle permettra de selectionner ce que l'on veut faire : 
		- Changer le nombre de joueur et leurs pseudos
		- Choisir le Backlog
		- Choisir le mode
		- Choisir si l'on veut un chrono ainsi que la valeur de celui-ci
	"""

	def __init__(self):
		Event.__init__(self)

		self.setNbPlayerEvent = SetNbPlayerEvent()
		self.setNameEvent     = SetNameEvent()
		self.setBacklogEvent  = SetBacklogEvent()
		self.setModeEvent     = SetModeEvent()
		self.setChronoEvent   = SetChronoEvent()

		self.setNbPlayer = False
		self.setName = False
		self.setBacklog = False
		self.setMode = False
		self.setChrono = False
		self.resetSelect()

	def event(self, game):
		"""
		Methode qui lance le menu de selection des divers paramètre du jeu avant le lancement de celui-ci
		"""

		self.resetSelect()
		self.param = self.extractParam()
		game.loadBacklog(self)
		# Si le Backlog sauvegarder dans param est complet, on le dé-selectionne pour eviter l'écrasement non-volontaire
		if self.param['backlog'] != -1:
			if game.testBacklog[game.listBacklog[self.param['backlog']]][1][1] == game.testBacklog[game.listBacklog[self.param['backlog']]][1][2]:
				self.param['backlog'] = -1

		while game.premainOn:

			for event in pygame.event.get():

				if event.type == MOUSEMOTION:
					self.findSelection(event.pos[0], event.pos[1])

				if event.type == MOUSEBUTTONDOWN:
					if self.select['nbPlayer']    : self.setNbPlayer = True
					if self.select['setName']     : self.setName = True
					if self.select['setBacklog']  : self.setBacklog = True
					if self.select['setMode']     : self.setMode = True
					if self.select['cocheChrono'] : self.param['cocheChrono'] = abs(1 - self.param['cocheChrono'])
					if self.select['setChrono']   : self.setChrono = True
					if self.select['lezgo']:
						if self.param['backlog'] != -1: # Verifie que l'on selectionne bien un backlog (On pourrait peut-etre ajouter un message sur l'écran)
							game.premainOn, game.mainOn = False, True 
							self.saveParam(game)
						else:
							if self.param['cochevolume'] == 1 : self.imp.sound.wrong.play()

				if event.type == KEYDOWN:
					if event.key == K_ESCAPE : game.premainOn, game.menuOn = False, True

				if event.type == QUIT:
					game.gameOn, game.premainOn = False, False

			self.blitage(game)

			if self.setNbPlayer : self.setNbPlayerEvent.event(game, self)
			if self.setName     : self.setNameEvent.event(game, self)
			if self.setBacklog  : self.setBacklogEvent.event(game, self)
			if self.setMode     : self.setModeEvent.event(game, self)
			if self.setChrono   : self.setChronoEvent.event(game, self)

	def findSelection(self, x, y):
		"""
		Methode qui permet d'observer si la souris sélectionne un choix
		"""
		if   self.inBox(x, y, self.imp.data.nbPlayer['box'])   : self.select['nbPlayer'] = 1
		elif self.inBox(x, y, self.imp.data.setName['box'])    : self.select['setName'] = 1
		elif self.inBox(x, y, self.imp.data.setBacklog['box']) : self.select['setBacklog'] = 1
		elif self.inBox(x, y, self.imp.data.setMode['box'])    : self.select['setMode'] = 1
		elif self.inBox(x, y, self.imp.data.lezgo['box'])      : self.select['lezgo'] = 1
		elif self.inBox(x, y, self.imp.data.cocheChrono['box'])   : self.select['cocheChrono'] = 1
		elif self.inBox(x, y, self.imp.data.setChrono['box'])    : self.select['setChrono'] = 1
		else : self.resetSelect()

	def resetSelect(self):
		"""
		Methode qui re-initialise le dict select
		"""
		self.select = {
			'player' : 0, 'nbPlayer' : 0, 'setName' : 0,
			'backlog' : 0, 'setBacklog' : 0,
			'mode' : 0, 'setMode' : 0,
			'chrono' : 0, 'cocheChrono' : 0, 'setChrono' : 0,
			'lezgo' : 0}

	def strChrono(self):
		return f"{int(self.param['time']//60):01}'{int(self.param['time']%60):02}\""

	def blitage(self, game):
		"""
		Methode qui permet de rafraichir le display et d'afficher la nouvelle frame 
		"""
		niqLezgo = 2 * (self.param['backlog'] == -1) # Met le bouton en rouge si il n'y a pas de backlog saisi

		game.ds.blit(self.imp.image.back_main, (0, 0))
		self.labelisation(game.ds, self.imp.font.roboto54, "Paramètre", (222, 222, 222), (0, 0), (1600, 100))

		self.blitBox(game.ds, self.imp.data.player,   self.select['player'])
		self.blitBox(game.ds, self.imp.data.nbPlayer, self.select['nbPlayer'], text=str(self.param['nb_name']))
		self.blitBox(game.ds, self.imp.data.setName,  self.select['setName'])

		self.blitBox(game.ds, self.imp.data.backlog,    self.select['backlog'])
		self.blitBox(game.ds, self.imp.data.setBacklog, self.select['setBacklog'], text=game.listBacklog[self.param['backlog']])

		self.blitBox(game.ds, self.imp.data.mode,    self.select['mode'])
		self.blitBox(game.ds, self.imp.data.setMode, self.select['setMode'], text=self.imp.data.listMode['text'][self.param['mode']])

		self.blitBox(game.ds, self.imp.data.chrono,   self.select['chrono'])
		self.blitBox(game.ds, self.imp.data.cocheChrono, self.select['cocheChrono'] + self.param['cocheChrono']*2)
		self.blitBox(game.ds, self.imp.data.setChrono,  self.select['setChrono'], text=self.strChrono())

		self.blitBox(game.ds, self.imp.data.lezgo, self.select['lezgo'] + niqLezgo)

		self.blitFPS(game.ds)
		pygame.display.flip()





class SetNbPlayerEvent(Event):
	"""
	Class utilisé par PremainEvent pour le changement du nombre de joueur
	"""

	def __init__(self):

		Event.__init__(self)


	def event(self, game, premainEvent):
		"""
		Methode qui lance l'evenement de changement de nombre de joueurs
		"""
		premainEvent.param['nb_name'] = str(premainEvent.param['nb_name'])
		premainEvent.resetSelect()
		self.select = 0
		self.param = premainEvent.param

		while premainEvent.setNbPlayer:

			for event in pygame.event.get():

				if event.type == MOUSEMOTION:
					self.select = 0
					# Observation de la souris lorsqu'elle passe sur Valider
					if self.inBox(event.pos[0], event.pos[1], self.imp.data.confirmNb['box']) : self.select = 1

				if event.type == MOUSEBUTTONDOWN:
					# Met à jour le pseudo si on appuie clique sur Valider
					if self.select == 1:
						premainEvent.param['nb_name'] = min(int(premainEvent.param['nb_name']), self.imp.data.maxPlayer)
						premainEvent.param['nb_name'] = max(int(premainEvent.param['nb_name']), self.imp.data.minPlayer)
						premainEvent.setNbPlayer = False


				if event.type == KEYDOWN:

					if event.key == K_ESCAPE:
						premainEvent.param['nb_name'] = int(premainEvent.param['nb_name'])
						premainEvent.setNbPlayer = False

					elif event.key in self.imp.data.keyValNUM.keys():
						if premainEvent.param['nb_name'] == '0' : premainEvent.param['nb_name'] = ''
						premainEvent.param['nb_name'] = str(premainEvent.param['nb_name']) + self.imp.data.keyValNUM[event.key]

					elif event.key == K_BACKSPACE:
						premainEvent.param['nb_name'] = str(premainEvent.param['nb_name'])[:-1]
						if len(premainEvent.param['nb_name']) == 0 : premainEvent.param['nb_name'] = '0'

					elif event.key == K_RETURN or event.key == K_KP_ENTER:
						premainEvent.param['nb_name'] = min(int(premainEvent.param['nb_name']), self.imp.data.maxPlayer)
						premainEvent.param['nb_name'] = max(int(premainEvent.param['nb_name']), self.imp.data.minPlayer)
						premainEvent.setNbPlayer = False

				if event.type == QUIT:
					game.gameOn, game.premainOn, setNbPlayer = False, False, False

			self.blitage(game, premainEvent)

	def blitage(self, game, premainEvent):
		"""
		Methode qui permet de rafraichir le display et d'afficher la nouvelle frame 
		"""
		game.ds.blit(self.imp.image.back_main, (0, 0))
		self.labelisation(game.ds, self.imp.font.roboto54, "Paramètre", (222, 222, 222), (0, 0), (1600, 100))

		self.blitBox(game.ds, self.imp.data.player,   premainEvent.select['player'])
		self.blitBox(game.ds, self.imp.data.nbPlayer, 1, text=str(premainEvent.param['nb_name']))
		self.blitBox(game.ds, self.imp.data.setName,  premainEvent.select['setName'])

		self.blitBox(game.ds, self.imp.data.backlog,    premainEvent.select['backlog'])
		self.blitBox(game.ds, self.imp.data.setBacklog, premainEvent.select['setBacklog'], text=game.listBacklog[premainEvent.param['backlog']])

		self.blitBox(game.ds, self.imp.data.mode,    premainEvent.select['mode'])
		self.blitBox(game.ds, self.imp.data.setMode, premainEvent.select['setMode'], text=self.imp.data.listMode['text'][premainEvent.param['mode']])

		self.blitBox(game.ds, self.imp.data.chrono,   premainEvent.select['chrono'])
		self.blitBox(game.ds, self.imp.data.cocheChrono, premainEvent.select['cocheChrono'] + premainEvent.param['cocheChrono']*2)
		self.blitBox(game.ds, self.imp.data.setChrono,  premainEvent.select['setChrono'], text=premainEvent.strChrono())

		self.blitBox(game.ds, self.imp.data.lezgo,     premainEvent.select['lezgo'])
		self.blitBox(game.ds, self.imp.data.confirmNb, self.select)

		self.blitFPS(game.ds)
		pygame.display.flip()





class SetNameEvent(Event):
	"""
	Class utilisé par PremainEvent pour changer le nom des joueurs
	"""

	def __init__(self):
		Event.__init__(self)


	def event(self, game, premainEvent):
		"""
		Methode qui lance le menu de changement de pseudo des joueurs
		"""
		premainEvent.resetSelect()
		self.select = None
		self.confirm = 0 # Ecouteur Valider
		self.retour  = 0 # Ecouteur Retour
		self.playerOnWrite = None
		self.lshift = False
		self.param = premainEvent.param
		self.niq = [0]*premainEvent.param['nb_name'] + [2]*(self.imp.data.maxPlayer-premainEvent.param['nb_name'])

		while premainEvent.setName:

			for event in pygame.event.get():

				if event.type == MOUSEMOTION:
					self.retour = 0
					if self.inBox(event.pos[0], event.pos[1], self.imp.data.retour['box']) : self.retour = 1	# Survol Retour

					self.select = None
					if self.playerOnWrite is None:
						self.select = None
						for i, box in enumerate(self.imp.data.listName['box']):
							if self.inBox(event.pos[0], event.pos[1], box) : self.select = i						# Survol un des noms de participant
					else:
						# Observation de la souris lorsqu'elle passe sur Valider
						self.confirm = 0
						if self.inBox(event.pos[0], event.pos[1], self.imp.data.confirmName['box']) : self.confirm = 1

				if event.type == MOUSEBUTTONDOWN:
					if self.select is not None and self.playerOnWrite is None:
						self.playerOnWrite = self.select
						self.playerOnPreName = premainEvent.param['list_name'][self.select]
					# Met à jour le pseudo si on appuie clique sur Valider
					elif self.playerOnWrite is not None and self.confirm == 1:
						if len(premainEvent.param['list_name'][self.playerOnWrite]) == 0 :
							premainEvent.param['list_name'][self.playerOnWrite] = f"Player{self.playerOnWrite}"
						self.playerOnWrite = None
					elif self.retour == 1: # Si on appuie sur Retour
						if self.playerOnWrite is not None: # Si on appuie alors que l'on est en train de modif un pseudo 
							if self.param['cochevolume'] == 1 : self.imp.sound.wrong.play()
						else:
							premainEvent.setName = False


				if event.type == KEYDOWN:
					if event.key == K_ESCAPE and self.playerOnWrite is None: 
						premainEvent.setName = False

					# Si on est en train de modifier un pseudo :
					elif self.playerOnWrite is not None:

						# Si on appuie sur Escape, on remet le nom avant tout changement (qui était enregistrer dans playerOnPreName)
						if event.key == K_ESCAPE:
							premainEvent.param['list_name'][self.playerOnWrite] = self.playerOnPreName
							self.playerOnWrite = None

						# Ajout de la lettre si une touche du clavier est dans la liste des touche importer dans 'self.imp.data.keyVal'
						elif event.key in self.imp.data.keyVal.keys():
							if self.lshift: # Mettre la lettre en majuscule si LSHIFT en maintenue
								premainEvent.param['list_name'][self.playerOnWrite] += self.imp.data.keyValCAP[event.key]
							else:           # Sinon, mettre la lettre en minuscule (par default)
								premainEvent.param['list_name'][self.playerOnWrite] += self.imp.data.keyVal[event.key]

						# On prend en compte l'appuie sur LSHIFT pour mettre une lettre en majuscule
						elif event.key == K_LSHIFT:
							self.lshift = True

						# Efface le dernier caractère si on appuie sur BACKSPACE (c'est la touche effacer)
						elif event.key == K_BACKSPACE:
							if len(premainEvent.param['list_name'][self.playerOnWrite]) != 0: # Mais pas si c'est deja vide !
								premainEvent.param['list_name'][self.playerOnWrite] = premainEvent.param['list_name'][self.playerOnWrite][:-1]

						# Met à jour le pseudo si on appuie sur RETURN / KP_ENTER (la touche entrer du clavier / du numpad)
						# On pourrait peut-etre mettre ici un controle sur le contenu du nom du joueur ?
						elif event.key == K_RETURN or event.key == K_KP_ENTER:
							if len(premainEvent.param['list_name'][self.playerOnWrite]) == 0 :
								premainEvent.param['list_name'][self.playerOnWrite] = f"Player{self.playerOnWrite}"
							self.playerOnWrite = None

				if event.type == KEYUP:
					# On prend en compte le relachement le LSHIFT
					if event.key == K_LSHIFT:
						self.lshift = False

				if event.type == QUIT:
					game.gameOn, game.premainOn, premainEvent.setName = False, False, False

			self.blitage(game, premainEvent)


	def blitage(self, game, premainEvent):
		"""
		Methode qui permet de rafraichir le display et d'afficher la nouvelle frame
		"""
		game.ds.blit(self.imp.image.back_main, (0, 0))
		self.labelisation(game.ds, self.imp.font.roboto54, "Choix Nom des joueurs", (222, 222, 222), (0, 0), (1600, 100))

		for i in range(10):
			activ = (i == self.select) * 1
			game.ds.blit(self.imp.data.listName['images'][activ + self.niq[i]], self.imp.data.listName['imgBox'][i][activ + self.niq[i]])
			self.labelisation(game.ds, 
				self.imp.data.listName['font'],
				premainEvent.param['list_name'][i], 
				self.imp.data.listName['color'],
				self.imp.data.listName['box'][i][0], self.imp.data.listName['box'][i][1], position='center')

		if self.playerOnWrite is not None:
			self.blitBox(game.ds, self.imp.data.confirmName, self.confirm)

		self.blitBox(game.ds, self.imp.data.retour, self.retour + (self.playerOnWrite is not None)*2)

		self.blitFPS(game.ds)
		pygame.display.flip()		





class SetBacklogEvent(Event):
	"""
	Class utilisé par PremainEvent pour changer de Backlog
	"""

	def __init__(self):
		Event.__init__(self)
		self.eraseBacklogEvent = EraseBacklogEvent()


	def event(self, game, premainEvent):
		"""
		Methode qui lance le menu de selection de changement de Backlog
		"""
		self.select = None
		self.param = premainEvent.param
		premainEvent.resetSelect()

		while premainEvent.setBacklog:

			for event in pygame.event.get():

				if event.type == MOUSEMOTION:
					self.select = None
					for i, box in enumerate(game.listBack['box']):
						if self.inBox(event.pos[0], event.pos[1], box) : self.select = i

				if event.type == MOUSEBUTTONDOWN:
					if self.select is not None : 
						premainEvent.setBacklog = False
						# On regarde si le backlog est deja complet (nombre fini == nombre total)
						if game.testBacklog[game.listBacklog[self.select]][1][1] == game.testBacklog[game.listBacklog[self.select]][1][2]:
							# On lance l'evenement de choix d'effacement ou pas de ce backlog complet
							self.eraseBacklogEvent.event(game, premainEvent, self)
						premainEvent.param['backlog'] = self.select
						return None

				if event.type == KEYDOWN:
					if event.key == K_ESCAPE : premainEvent.setBacklog = False

				if event.type == QUIT:
					game.gameOn, game.premainOn, premainEvent.setBacklog = False, False, False

			self.blitage(game)


	def blitage(self, game):
		"""
		Methode qui permet de rafraichir le display et d'afficher la nouvelle frame
		"""
		game.ds.blit(self.imp.image.back_main, (0, 0))
		self.labelisation(game.ds, self.imp.font.roboto54, "Choix Backlog", (222, 222, 222), (0, 0), (1600, 100))

		for i, backlog in enumerate(game.listBacklog[:-1]):
			activ = (i == self.select) * 1
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





class EraseBacklogEvent(Event):
	"""
	Class utiliser par la SetBacklogEvent pour effacer (ou non) un backlog complet
	"""

	def __init__(self):
		Event.__init__(self)


	def event(self, game, premainEvent, setBacklogEvent):
		"""
		Methode qui lance le menu de choix d'effacement de backlog
		"""
		self.eraseEvent = True
		self.param = premainEvent.param
		self.selectErase = {'Non':0, 'Oui':0}

		while self.eraseEvent:

			for event in pygame.event.get():

				if event.type == MOUSEMOTION:
					self.selectErase = {'Non':0, 'Oui':0}
					if self.inBox(event.pos[0], event.pos[1], self.imp.data.eraseOui['box']) : self.selectErase['Oui'] = 1
					if self.inBox(event.pos[0], event.pos[1], self.imp.data.eraseNon['box']) : self.selectErase['Non'] = 1

				if event.type == MOUSEBUTTONDOWN:
					if sum(self.selectErase.values()) > 0: 
						self.eraseEvent = False
						if self.selectErase['Oui'] == 1 :
							backlogName = game.listBacklog[setBacklogEvent.select]
							backlogErase = game.testBacklog[backlogName][0]
							for key in backlogErase.keys():
								backlogErase[key] = -1
							import_json.writeJson(backlogName, backlogErase)
							game.loadBacklog(setBacklogEvent)
						else : 
							setBacklogEvent.select = -1
						return None

				if event.type == KEYDOWN:
					pass #PAS DESCAPE ICI :(((

				if event.type == QUIT:
					game.gameOn, game.premainOn, premainEvent.setBacklog, self.eraseEvent = False, False, False, False

			self.blitage(game)


	def blitage(self, game):
		"""
		Methode qui permet de rafraichir le display et d'afficher la nouvelle frame
		"""
		game.ds.blit(self.imp.image.back_main, (0, 0))
		self.labelisation(game.ds, self.imp.font.roboto54, "Attention !", (222, 222, 222), (0, 0), (1600, 100))

		self.blitBox(game.ds, self.imp.data.eraseQuestion, 0)
		self.labelisation(game.ds, self.imp.font.roboto32, 'vous vous tout recommencer ?', (0, 0, 0), (400, 240), (800, 400))

		self.blitBox(game.ds, self.imp.data.eraseOui, self.selectErase['Oui'])
		self.blitBox(game.ds, self.imp.data.eraseNon, self.selectErase['Non'])

		self.blitFPS(game.ds)
		pygame.display.flip()





class SetModeEvent(Event):
	"""
	Class utilisé par PremainEvent pour la selection du mode de jeu
	"""

	def __init__(self):
		Event.__init__(self)
		self.select = None


	def event(self, game, premainEvent):
		"""
		Methode qui lance le menu de selection du mode de jeu
		"""
		self.select = None
		self.param = premainEvent.param

		while premainEvent.setMode:

			for event in pygame.event.get():

				if event.type == MOUSEMOTION:
					self.select = None
					for i, box in enumerate(self.imp.data.listMode['box']):
						if self.inBox(event.pos[0], event.pos[1], box) : self.select = i

				if event.type == MOUSEBUTTONDOWN:
					if self.select is not None : 
						premainEvent.setMode = False
						premainEvent.param['mode'] = self.select
						premainEvent.resetSelect()
						return None

				if event.type == KEYDOWN:
					if event.key == K_ESCAPE : premainEvent.setMode = False

				if event.type == QUIT:
					game.gameOn, game.premainOn, premainEvent.setMode = False, False, False

			self.blitage(game)


	def blitage(self, game):
		"""
		Methode qui permet de rafraichir le display et d'afficher la nouvelle frame
		"""
		game.ds.blit(self.imp.image.back_main, (0, 0))
		self.labelisation(game.ds, self.imp.font.roboto54, "Choix Mode", (222, 222, 222), (0, 0), (1600, 100))

		for i, mode in enumerate(self.imp.data.listMode['text']):
			activ = (i == self.select) * 1
			game.ds.blit(self.imp.data.listMode['images'][activ], self.imp.data.listMode['imgBox'][i][activ])
			self.labelisation(game.ds, 
				self.imp.data.listMode['font'], self.imp.data.listMode['text'][i], self.imp.data.listMode['color'],
				self.imp.data.listMode['box'][i][0], self.imp.data.listMode['box'][i][1])

		self.blitFPS(game.ds)
		pygame.display.flip()





class SetChronoEvent(Event):
	"""
	Class utilisé par PremainEvent pour le changement de temps du chrono
	"""

	def __init__(self):
		Event.__init__(self)


	def event(self, game, premainEvent):
		"""
		Methode qui lance l'evenement de changement de temps du chrono
		"""
		premainEvent.param['time'] = str(premainEvent.param['time'])
		premainEvent.resetSelect()
		self.param = premainEvent.param
		self.select = 0

		while premainEvent.setChrono:

			for event in pygame.event.get():

				if event.type == MOUSEMOTION:
					self.select = 0
					# Observation de la souris lorsqu'elle passe sur Valider
					if self.inBox(event.pos[0], event.pos[1], self.imp.data.confirmNb['box']) : self.select = 1

				if event.type == MOUSEBUTTONDOWN:
					# Met à jour le pseudo si on appuie clique sur Valider
					if self.select == 1:
						premainEvent.param['time'] = min(int(premainEvent.param['time']), self.imp.data.maxTimeChrono)
						premainEvent.param['time'] = max(int(premainEvent.param['time']), self.imp.data.minTimeChrono)
						premainEvent.setChrono = False


				if event.type == KEYDOWN:

					if event.key == K_ESCAPE:
						premainEvent.param['time'] = int(premainEvent.param['time'])
						premainEvent.setChrono = False

					elif event.key in self.imp.data.keyValNUM.keys():
						if premainEvent.param['time'] == '0' : premainEvent.param['time'] = ''
						premainEvent.param['time'] = str(premainEvent.param['time']) + self.imp.data.keyValNUM[event.key]

					elif event.key == K_BACKSPACE:
						premainEvent.param['time'] = str(premainEvent.param['time'])[:-1]
						if len(premainEvent.param['time']) == 0 : premainEvent.param['time'] = '0'

					elif event.key == K_RETURN or event.key == K_KP_ENTER:
						premainEvent.param['time'] = min(int(premainEvent.param['time']), self.imp.data.maxTimeChrono)
						premainEvent.param['time'] = max(int(premainEvent.param['time']), self.imp.data.minTimeChrono)
						premainEvent.setChrono = False

				if event.type == QUIT:
					game.gameOn, game.premainOn, premainEvent.setChrono = False, False, False

			self.blitage(game, premainEvent)

	def blitage(self, game, premainEvent):
		"""
		Methode qui permet de rafraichir le display et d'afficher la nouvelle frame 
		"""
		game.ds.blit(self.imp.image.back_main, (0, 0))
		self.labelisation(game.ds, self.imp.font.roboto54, "Paramètre", (222, 222, 222), (0, 0), (1600, 100))

		self.blitBox(game.ds, self.imp.data.player,   premainEvent.select['player'])
		self.blitBox(game.ds, self.imp.data.nbPlayer, premainEvent.select['nbPlayer'], text=str(premainEvent.param['nb_name']))
		self.blitBox(game.ds, self.imp.data.setName,  premainEvent.select['setName'])

		self.blitBox(game.ds, self.imp.data.backlog,    premainEvent.select['backlog'])
		self.blitBox(game.ds, self.imp.data.setBacklog, premainEvent.select['setBacklog'], text=game.listBacklog[premainEvent.param['backlog']])

		self.blitBox(game.ds, self.imp.data.mode,    premainEvent.select['mode'])
		self.blitBox(game.ds, self.imp.data.setMode, premainEvent.select['setMode'], text=self.imp.data.listMode['text'][premainEvent.param['mode']])

		self.blitBox(game.ds, self.imp.data.chrono,   premainEvent.select['chrono'])
		self.blitBox(game.ds, self.imp.data.cocheChrono, premainEvent.select['cocheChrono'] + premainEvent.param['cocheChrono']*2)
		self.blitBox(game.ds, self.imp.data.setChrono,  1, text=f"{premainEvent.param['time']} sec.")

		self.blitBox(game.ds, self.imp.data.lezgo,     premainEvent.select['lezgo'])
		self.blitBox(game.ds, self.imp.data.confirmNb, self.select)

		self.blitFPS(game.ds)
		pygame.display.flip()
