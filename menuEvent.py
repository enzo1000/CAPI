import pygame
import numpy as np
from pygame.locals import *

from event import Event

from fil_to_delete import dico, revers


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

	def event(self, game):
		"""
		Methode qui lance le menu de l'application
		"""

		self.resetSelect()
		self.debug = ''

		while game.menuOn:

			for event in pygame.event.get():

				# Detecte le déplacement de la souris
				if event.type == MOUSEMOTION: 
					self.findSelection(event.pos[0], event.pos[1])

				# Detecte le clique de la souris
				if event.type == MOUSEBUTTONDOWN:
					if self.select['begin']  : game.menuOn, game.premainOn = False, True
					if self.select['langue'] : print('Langue Event Not Make')
					if self.select['quit']   : game.gameOn, game.menuOn = False, False

				# Detecte l'appuie sur une touche du clavier
				if event.type == KEYDOWN:
					if event.key == K_ESCAPE : 
						game.gameOn, game.menuOn = False, False
					else :
						if event.key in revers.keys():
							print(f"Pour l'entree : {event.key} -> {revers[event.key]}")
						else:
							print(f"Entree {event.key} inconnu")

				# Detecte le clique sur la croix qui ferme l'appli
				if event.type == QUIT:
					game.gameOn, game.menuOn = False, False

			self.blitage(game.ds)


	def findSelection(self, x, y):
		"""
		Methode qui permet d'observer si la souris sélectionne un choix
		"""
		if   self.inBox(x, y, self.imp.data.menu_begin['box']) : self.select['begin']  = 1
		elif self.inBox(x, y, self.imp.data.menu_langue['box']) : self.select['langue'] = 1
		elif self.inBox(x, y, self.imp.data.menu_quit['box']) : self.select['quit']   = 1 
		else : self.resetSelect()

	def resetSelect(self):
		"""
		Methode qui re-initialise le dict select
		"""
		self.select = {
			'begin'  : 0,
			'langue' : 0,
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
		self.blitBox(display, self.imp.data.menu_langue, self.select['langue'])

		#Blit la zone 'Quitter'
		self.blitBox(display, self.imp.data.menu_quit, self.select['quit'])

		# Blit les FPS
		self.blitFPS(display)
		pygame.display.flip()

