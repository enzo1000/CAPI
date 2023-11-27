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
		+ *** Tout les attributs de la class mère Event
		- select [dict] : dict contenant le choix pointer par la souris
	
	Methode : 
		- event(game)         : méthode qui va permettre de lancer le menu
		- findSelection(x, y) : methode qui permet d'observer si la souris sélectionne un choix
		- resetSelect()       : méthode qui re-initialise le dict select
		- blitage(display)    : méthode qui permet de rafraichir le display et d'afficher la nouvelle frame 
	"""

	def __init__(self):
		Event.__init__(self)
		self.resetSelect()

	def event(self, game):

		self.resetSelect()

		while game.menuOn:

			for event in pygame.event.get():

				if event.type == MOUSEMOTION: 
					self.findSelection(event.pos[0], event.pos[1])

				if event.type == MOUSEBUTTONDOWN:
					if self.select['begin']  : game.menuOn, game.premainOn = False, True
					if self.select['langue'] : print('Langue Event Not Make')
					if self.select['quit']   : game.gameOn, game.menuOn = False, False

				if event.type == KEYDOWN:
					if event.key == K_ESCAPE : game.gameOn, game.menuOn = False, False

				if event.type == QUIT:
					game.gameOn, game.menuOn = False, False

			self.blitage(game.ds)


	def findSelection(self, x, y):
		if   self.inBox(x, y, self.imp.data.menu_begin['box']) : self.select['begin']  = 1
		elif self.inBox(x, y, self.imp.data.menu_langue['box']) : self.select['langue'] = 1
		elif self.inBox(x, y, self.imp.data.menu_quit['box']) : self.select['quit']   = 1 
		else : self.resetSelect()

	def resetSelect(self):
		self.select = {
			'begin'  : 0,
			'langue' : 0,
			'quit'   : 0}


	def blitage(self, display):

		# Blit le background
		display.blit(self.imp.image.back_main, (0, 0))

		# Blit le text 'Menu'
		self.labelisation(display, self.imp.font.roboto54, "Menu", (222, 222, 222), (0, 0), (1600, 100))

		# Blit la zone 'Commencer'
		self.blitBox(display, self.imp.data.menu_begin, self.select['begin'])

		# Blit la zone 'Langue'
		self.blitBox(display, self.imp.data.menu_langue, self.select['langue'])

		#Blit la zone 'Quitter'
		self.blitBox(display, self.imp.data.menu_quit, self.select['quit'])

		# Blit les FPS
		self.blitFPS(display)
		pygame.display.flip()

