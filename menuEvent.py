import pygame
import numpy as np
from pygame.locals import *

from event import Event

class MenuEvent(Event):
	"""
	Classe MenuEvent hérité de Event
	Cette classe permet de gérer le menu de notre application. 
	Elle permettra de selectionner ce que l'on veut faire : 
		- Commencer une partie de planning poker
		- Changer la langue (Pour l'instant que Fr disponible)
		- Quitter l'application

	Param Init :
		- game [GameClass] : Objet de class GameClass, qui contient les caractéristique physique de l'appli (le display ...)

	Attribut :
		+ *** Tout les attributs décrites dans la class mère Event
		- select [dict] : dict contenant le choix pointer par la souris
	
	Methode : 
		+ *** Toutes les methodes décrites dans la classe mère Event
		- event(game)         : Methode qui lance le menu de l'application
		- findSelection(x, y) : Methode qui permet d'observer si la souris sélectionne un choix
		- resetSelect()       : Methode qui re-initialise le dict select
		- blitage(display)    : Methode qui permet de rafraichir le display et d'afficher la nouvelle frame 
	"""

	def __init__(self):
		Event.__init__(self)
		self.resetSelect()
		self.setOptionEvent = SetOptionEvent()
		self.setOption = False

	def event(self, game):
		"""
		Methode qui lance le menu de l'application
		"""

		self.resetSelect()
		self.debug = ''
		game.loadBacklog(self)
		self.param = self.extractParam()

		while game.menuOn:

			for event in pygame.event.get():

				# Detecte le déplacement de la souris
				if event.type == MOUSEMOTION: 
					self.findSelection(event.pos[0], event.pos[1])

				# Detecte le clique de la souris
				if event.type == MOUSEBUTTONDOWN:
					if self.select['begin']  : game.menuOn, game.premainOn = False, True
					if self.select['option'] : self.setOption = True
					if self.select['quit']   : game.gameOn, game.menuOn = False, False

				# Detecte l'appuie sur une touche du clavier
				if event.type == KEYDOWN:
					if event.key == K_ESCAPE : 
						game.gameOn, game.menuOn = False, False

				# Detecte le clique sur la croix qui ferme l'appli
				if event.type == QUIT:
					game.gameOn, game.menuOn = False, False


			if self.setOption : self.setOptionEvent.event(game, self)

			self.blitage(game.ds)


	def findSelection(self, x, y):
		"""
		Methode qui permet d'observer si la souris sélectionne un choix
		"""
		if   self.inBox(x, y, self.imp.data.menu_begin['box']) : self.select['begin']  = 1
		elif self.inBox(x, y, self.imp.data.menu_langue['box']) : self.select['option'] = 1
		elif self.inBox(x, y, self.imp.data.menu_quit['box']) : self.select['quit']   = 1 
		else : self.resetSelect()

	def resetSelect(self):
		"""
		Methode qui re-initialise le dict select
		"""
		self.select = {
			'begin'  : 0,
			'option' : 0,
			'quit'   : 0}


	def blitage(self, display):
		"""
		Methode qui permet de rafraichir le display et d'afficher la nouvelle frame 
		"""

		# Blit le background
		display.blit(self.imp.image.back_main, (0, 0))

		# Blit le text 'Menu'
		self.labelisation(display, self.imp.font.roboto54, "Menu", (222, 222, 222), (0, 0), (1600, 100))

		# Blit la zone 'Commencer'
		self.blitBox(display, self.imp.data.menu_begin, self.select['begin'])

		# Blit la zone 'Langue'
		self.blitBox(display, self.imp.data.menu_langue, self.select['option'])

		#Blit la zone 'Quitter'
		self.blitBox(display, self.imp.data.menu_quit, self.select['quit'])

		# Blit les FPS
		self.blitFPS(display)
		pygame.display.flip()





class SetOptionEvent(Event):
	"""
	Class utilisé par MenuEvent pour le changement des options du jeu : FPS et paramètres sonore
	"""

	def __init__(self):
		Event.__init__(self)
		self.setVolumeEvent = SetVolumeEvent()
		self.setVolume = False
		self.resetSelect()

	def event(self, game, menuEvent):
		"""
		Methode qui lance le menu d'option
		"""

		self.param = menuEvent.param

		while menuEvent.setOption:

			for event in pygame.event.get():

				if event.type == MOUSEMOTION:
					self.findSelection(event.pos[0], event.pos[1])

				if event.type == MOUSEBUTTONDOWN:
					if self.select['cochevolume']    : menuEvent.param['cochevolume'] = abs(1 - menuEvent.param['cochevolume'])
					if self.select['setvolume']      : self.setVolume = True
					if self.select['cocheshowFPS']   : menuEvent.param['showFPS'] = abs(1 - menuEvent.param['showFPS'])
					if self.select['cochecapFPS']    : menuEvent.param['cochecapFPS'] = abs(1 - menuEvent.param['cochecapFPS'])
					if self.select['valider']        : menuEvent.setOption = False

				if event.type == KEYDOWN:
					if event.key == K_ESCAPE : menuEvent.setOption = False
					menuEvent.saveParam(game)

				if event.type == QUIT:
					game.gameOn, game.menuOn, menuEvent.setOption = False, False, False
					menuEvent.saveParam(game)

			self.blitage(game, menuEvent)

			if self.setVolume : self.setVolumeEvent.event(game, self)

		# On save param en quittant SetOptionEvent
		self.saveParam(game)

	def findSelection(self, x, y):
		"""
		Methode qui permet d'observer si la souris sélectionne un choix
		"""
		if   self.inBox(x, y, self.imp.data.cocheVolume['box'])   : self.select['cochevolume'] = 1
		elif self.inBox(x, y, self.imp.data.setVolume['box'])    : self.select['setvolume'] = 1
		elif self.inBox(x, y, self.imp.data.cocheShowFPS['box']) : self.select['cocheshowFPS'] = 1
		elif self.inBox(x, y, self.imp.data.cocheCapFPS['box'])    : self.select['cochecapFPS'] = 1
		elif self.inBox(x, y, self.imp.data.validerOption['box'])    : self.select['valider'] = 1
		else : self.resetSelect()

	def resetSelect(self):
		"""
		Methode qui re-initialise le dict select
		"""
		self.select = {
			'cochecapFPS' : 0, 'cocheshowFPS' : 0, 
			'cochevolume' : 0, 'setvolume' : 0,
			'valider' : 0
			}


	def blitage(self, game, menuEvent):
		"""
		Methode qui permet de rafraichir le display et d'afficher la nouvelle frame 
		"""

		game.ds.blit(self.imp.image.back_main, (0, 0))
		self.labelisation(game.ds, self.imp.font.roboto54, "Option", (222, 222, 222), (0, 0), (1600, 100))

		self.blitBox(game.ds, self.imp.data.volume, 0)
		self.blitBox(game.ds, self.imp.data.cocheVolume, self.select['cochevolume'] + self.param['cochevolume']*2)
		self.blitBox(game.ds, self.imp.data.setVolume,  self.select['setvolume'], text=f"{self.param['setvolume']}%")

		self.blitBox(game.ds, self.imp.data.showFPS, 0)
		self.blitBox(game.ds, self.imp.data.cocheShowFPS, self.select['cocheshowFPS'] + menuEvent.param['showFPS']*2)
		
		self.blitBox(game.ds, self.imp.data.capFPSbox, 0)
		self.blitBox(game.ds, self.imp.data.cocheCapFPS, self.select['cochecapFPS'] + menuEvent.param['cochecapFPS']*2)
		
		self.blitBox(game.ds, self.imp.data.validerOption, self.select['valider'])

		self.blitFPS(game.ds)
		pygame.display.flip()






class SetVolumeEvent(Event):
	"""
	Class utilisé par SetOptionEvent pour modifier le volume sonore
	"""

	def __init__(self):
		Event.__init__(self)


	def event(self, game, setOptionEvent):
		"""
		Methode qui lance l'evenement pour modifier le volume sonore
		"""
		setOptionEvent.param['setvolume'] = str(setOptionEvent.param['setvolume'])
		# premainEvent.resetSelect()
		self.param = setOptionEvent.param
		self.select = 0

		while setOptionEvent.setVolume:

			for event in pygame.event.get():

				if event.type == MOUSEMOTION:
					self.select = 0
					# Observation de la souris lorsqu'elle passe sur Valider
					if self.inBox(event.pos[0], event.pos[1], self.imp.data.confirmNb['box']) : self.select = 1

				if event.type == MOUSEBUTTONDOWN:
					# Met à jour le pseudo si on appuie clique sur Valider
					if self.select == 1:
						setOptionEvent.param['setvolume'] = min(int(setOptionEvent.param['setvolume']), 100)
						setOptionEvent.param['setvolume'] = max(int(setOptionEvent.param['setvolume']), 0)
						setOptionEvent.setVolume = False


				if event.type == KEYDOWN:

					if event.key == K_ESCAPE:
						setOptionEvent.param['setvolume'] = int(setOptionEvent.param['setvolume'])
						setOptionEvent.setVolume = False

					elif event.key in self.imp.data.keyValNUM.keys():
						if setOptionEvent.param['setvolume'] == '0' : setOptionEvent.param['setvolume'] = ''
						setOptionEvent.param['setvolume'] = str(setOptionEvent.param['setvolume']) + self.imp.data.keyValNUM[event.key]

					elif event.key == K_BACKSPACE:
						setOptionEvent.param['setvolume'] = str(setOptionEvent.param['setvolume'])[:-1]
						if len(setOptionEvent.param['setvolume']) == 0 : setOptionEvent.param['setvolume'] = '0'

					elif event.key == K_RETURN or event.key == K_KP_ENTER:
						setOptionEvent.param['setvolume'] = min(int(setOptionEvent.param['setvolume']), 100)
						setOptionEvent.param['setvolume'] = max(int(setOptionEvent.param['setvolume']), 0)
						setOptionEvent.setVolume = False

				if event.type == QUIT:
					game.gameOn, game.menuOn, setOptionEvent.setVolume = False, False, False

			self.blitage(game, setOptionEvent)

		# Update le volume en quittant l'event SetVolumeEvent
		self.updateVolume(setOptionEvent.param['setvolume'])
		self.saveParam(game)
		setOptionEvent.resetSelect()

	def blitage(self, game, setOptionEvent):
		"""
		Methode qui permet de rafraichir le display et d'afficher la nouvelle frame 
		"""
		game.ds.blit(self.imp.image.back_main, (0, 0))
		self.labelisation(game.ds, self.imp.font.roboto54, "Option", (222, 222, 222), (0, 0), (1600, 100))

		self.blitBox(game.ds, self.imp.data.volume, 0)
		self.blitBox(game.ds, self.imp.data.cocheVolume, 0 + self.param['cochevolume']*2)
		self.blitBox(game.ds, self.imp.data.setVolume,  1, text=f"{setOptionEvent.param['setvolume']}%")

		self.blitBox(game.ds, self.imp.data.showFPS, 0)
		self.blitBox(game.ds, self.imp.data.cocheShowFPS, 0 + setOptionEvent.param['showFPS']*2)
		
		self.blitBox(game.ds, self.imp.data.capFPSbox, 0)
		self.blitBox(game.ds, self.imp.data.cocheCapFPS, 0 + setOptionEvent.param['cochecapFPS']*2)

		self.blitBox(game.ds, self.imp.data.validerOption, 0)
		self.blitBox(game.ds, self.imp.data.confirmNb, self.select)

		self.blitFPS(game.ds)
		pygame.display.flip()
