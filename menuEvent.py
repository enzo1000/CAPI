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
		self.param = self.extractParam()

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
		# self.setVolumeEvent = SetVolumeEvent()
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
					if self.select['setvolume']      : print('setvolume')
					if self.select['cocheshowFPS']   : menuEvent.param['showFPS'] = abs(1 - menuEvent.param['showFPS'])
					if self.select['cochecapFPS']    : menuEvent.param['cochecapFPS'] = abs(1 - menuEvent.param['cochecapFPS']) # self.setMode = True

				if event.type == KEYDOWN:
					if event.key == K_ESCAPE : menuEvent.setOption = False
					menuEvent.saveParam(game)

				if event.type == QUIT:
					game.gameOn, game.menuOn, menuEvent.setOption = False, False, False
					menuEvent.saveParam(game)

			self.blitage(game, menuEvent)

			# if self.setNbPlayer : self.setNbPlayerEvent.event(game, self)
			# if self.setName     : self.setNameEvent.event(game, self)
			# if self.setBacklog  : self.setBacklogEvent.event(game, self)
			# if self.setMode     : self.setModeEvent.event(game, self)
			# if self.setChrono   : self.setChronoEvent.event(game, self)

	def findSelection(self, x, y):
		"""
		Methode qui permet d'observer si la souris sélectionne un choix
		"""
		if   self.inBox(x, y, self.imp.data.cocheVolume['box'])   : self.select['cochevolume'] = 1
		elif self.inBox(x, y, self.imp.data.setVolume['box'])    : self.select['setvolume'] = 1
		elif self.inBox(x, y, self.imp.data.cocheShowFPS['box']) : self.select['cocheshowFPS'] = 1
		elif self.inBox(x, y, self.imp.data.cocheCapFPS['box'])    : self.select['cochecapFPS'] = 1
		else : self.resetSelect()

	def resetSelect(self):
		"""
		Methode qui re-initialise le dict select
		"""
		self.select = {
			'cochecapFPS' : 0, 'cocheshowFPS' : 0, 
			'cochevolume' : 0, 'setvolume' : 0
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
		

		# self.blitBox(game.ds, self.imp.data.validerOption, self.select['valider'])

		self.blitFPS(game.ds)
		pygame.display.flip()
