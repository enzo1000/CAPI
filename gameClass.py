import pygame
from pygame.locals import *
import import_json

class GameClass():
	"""
	Class GameClass : Permet de gérer plusieurs paramètre de l'appli, notament la gestion de la fenètre
	"""

	def __init__(self, displayXY, displayCaption, beginBy='menu'):
		pygame.init()

		# Dimension de la fenètre
		self.ds = pygame.display.set_mode(displayXY)
		# Nom de la fenètre
		pygame.display.set_caption(displayCaption)

		self.gameOn    = True

		self.menuOn    = False
		self.premainOn = False
		self.mainOn    = False
		
		if beginBy == 'menu'    : self.menuOn    = True
		if beginBy == 'premain' : self.premainOn = True
		if beginBy == 'main'    : self.mainOn    = True

	def loadBacklog(self, event):
		"""
		Methode permettant de load les backlog présent dans le dossier `./data_json/`
		"""

		# Importation des json
		self.testBacklog = import_json.findAllJson()
		self.listBacklog  = list(self.testBacklog.keys()) + ['-----']
		n = len(list(self.testBacklog.keys()))

		# Definition des caractéristiques d'affcihage pour la liste des backlog
		self.listBack = {'images' : event.imp.image.sprit_480_80,
			'imgBox': [((556, 250+100*i), (546, 248+100*i)) for i in range(n)],
			'text'  : list(self.testBacklog.keys()),
			'color' : event.imp.color.noir,
			'font'  : event.imp.font.roboto32,
			'box'   : [((560, 250 + 100*i), (480, 80)) for i in range(n)]}