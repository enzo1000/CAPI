import pygame
import time
import os
import numpy as np
from pygame.locals import *
from class_import import importation




class Event():
	"""
	Classe Event qui servira de classe mère pour les différents event
	"""

	def __init__(self):
		self.time0       = time.time()         # Date d'initialisation de l'event
		self.timeRefresh = time.time()         # Attribut qui permettra le calcul des FPS
		self.refreshFPS  = 0.5                 # Durée de rafraichissement de l'affichage des FPS
		self.spf         = np.ones(20)         # Liste contenant les 20 dernier SPF (Second Per Frame : 1/FPS)
		self.fps         = '---'               # Attribut qui contiendra les FPS ('---' avant le premier calcul)
		self.imp         = importation()       # Attribut qui contient la class importation, qui contient tout le contient audio-visuel
		self.clock       = pygame.time.Clock() # Attribut qui permettra de capper les FPS
		self.param       = self.extractParam()

		self.updateVolume(self.param['setvolume'])

		# try:
		# 	self.imp.sound.wrong.set_volume(0.1)
		# 	self.imp.sound.carte.set_volume(0.5)
		# except:
		# 	print("Audio non initialisé")



	def updateVolume(self, volume):

		try:
			self.imp.sound.wrong.set_volume(self.imp.sound.VolumeMaxWrong * volume / 100)
			self.imp.sound.carte.set_volume(self.imp.sound.VolumeMaxCarte * volume / 100)
		except:
			print("Audio non update")



	def blitFPS(self, ds):
		"""
		Methode qui permet de calculer et d'afficher les FPS
		"""

		self.spf[:-1], self.spf[-1] = self.spf[1:], time.time() - self.time0
		self.time0 = time.time()
		
		if time.time() - self.timeRefresh > self.refreshFPS:
			self.timeRefresh = time.time()
			self.fps = str(int(20 / np.sum(self.spf)))

		if self.param['showFPS'] == 1 : self.labelisation(ds, self.imp.font.roboto16, f"{self.fps:3} FPS", (222, 222, 222), (1600-64, 900-24), (64, 24))

		if self.param['cochecapFPS'] == 1 : self.clock.tick(self.imp.data.capFPS)

	
	def labelisation(self, display, font, text, color, X, dX, position='center'):
		"""
		Methode qui permet dafficher une texte avec les caractérisque demander en argument
			-> position 'center' : Le texte s'affiche au centre de la box donner
			-> position 'left'   : Le texte s'affiche vers la gauche de la box donner
		"""
		surface = font.render(text, True, color)
		if position == 'center' : rect = surface.get_rect(center  = (int(X[0] + dX[0]/2), int(X[1] + dX[1]/2)))
		if position == 'left'   : rect = surface.get_rect(midleft = (int(X[0])          , int(X[1] + dX[1]/2)))
		display.blit(surface, rect)


	def blitBox(self, display, data, select=0, text=None, position='center'):
		"""
		Methode permettant d'afficher un le visuel entier de data qui est donner dans les import
			-> si le texte est variable, il peut etre donner dans text, sinon, on prend celui indiquer dans l'import
		"""

		if text is None : text = data['text']

		display.blit(data['images'][select], data['imgBox'][select])
		self.labelisation(display, 
			data['font'],
			text, 
			data['color'],
			data['box'][0], data['box'][1], position=position)



	def blitTextBox(self, display, Box, colors, text, font):
		"""
		Methode permettant d'afficher un texte avec un rectangle de couleur derriere
			-> Ne doit etre utiliser en placaholder, car souvent le rendu est moyen
		"""
		surface_dessin = pygame.Surface(Box[1])
		surface_dessin.fill(colors[0])
		display.blit(surface_dessin, Box[0])
		self.labelisation(display, font, text, colors[1], Box[0], Box[1])


	def inBox(self, x, y, Box):
		"""
		Methode permettant de revoyer True si les coordonnéer (x, y) sont dans la box
			-> Utiliser surtout pour connaitre l'emplacement de la souris 
		"""

		if 0 < x - Box[0][0] < Box[1][0] and 0 < y - Box[0][1] < Box[1][1]:
			return True
		else:
			return False


	def extractParam(self, folder='data'):
		"""
		Methode permmetant d'extraire les donner paramètre
			-> Si le file est corrompu ou n'existe pas, il est recréer par défault
		"""

		if True in ['param.ini' in file for file in os.listdir(f"./{folder}/")]:
			try:
				param = {}
				f = open(f"./{folder}/param.ini", 'r').read().replace(' ', '').split('\n')[1:]
				param['mode']    = int(f[0].split(':')[1].split('[')[0])
				param['backlog'] = int(f[1].split(':')[1].split('[')[0])
				param['nb_name'] = int(f[2].split(':')[1])
				param['list_name'] = []
				for i in range(10):
					param['list_name'].append(f[3+i].split(':')[1])
				param['cocheChrono'] = int(f[13].split(':')[1])
				param['time']        = int(f[14].split(':')[1])
				param['cochecapFPS'] = int(f[15].split(':')[1])
				param['capFPS']      = int(f[16].split(':')[1])
				param['showFPS']     = int(f[17].split(':')[1])
				param['cochevolume'] = int(f[18].split(':')[1])
				param['setvolume']   = int(f[19].split(':')[1])
			except:
				param = {'mode' : 0, 'nb_name' : 2, 'backlog' : 0, 'list_name' : [f"Player{i+1}" for i in range(10)], 'cocheChrono' : 0, 'time' : 60, 'cochecapFPS':1, 'capFPS':60, 'showFPS':1, 'cochevolume':1, 'setvolume':50}
				print("WARNING : Probleme dans 'param.ini' -> création d'un nouveau fichier de paramètre")
		else:
			param = {'mode' : 0, 'nb_name' : 2, 'backlog' : 0, 'list_name' : [f"Player{i+1}" for i in range(10)], 'cocheChrono' : 0, 'time' : 60, 'cochecapFPS':1, 'capFPS':60, 'showFPS':1, 'cochevolume':1, 'setvolume':50}
			print("WARNING : Probleme dans 'param.ini' -> création d'un nouveau fichier de paramètre")

		return param


	def saveParam(self, game, folder='data'):
		"""
		Methode permettant de save les paramètre en cours
		"""

		f = open(f"./{folder}/param.ini", "w")
		f.write(f"Paramètre :\n")
		f.write(f"Mode          : {self.param['mode']} [{self.imp.data.listMode['text'][self.param['mode']]}]\n")
		f.write(f"BackLog       : {self.param['backlog']} [{game.listBacklog[self.param['backlog']]}]\n")
		f.write(f"Player number : {self.param['nb_name']}\n")
		[f.write(f"- Player {i+1} : {name}\n") for i, name in enumerate(self.param['list_name'])]
		f.write(f"Prise en compte du chrono : {self.param['cocheChrono']}\n")
		f.write(f"Temps chrono : {self.param['time']}\n")
		f.write(f"Cap FPS : {self.param['cochecapFPS']}\n")
		f.write(f"Valeur du cap : {self.param['capFPS']}\n")
		f.write(f"Afficher FPS : {self.param['showFPS']}\n")
		f.write(f"Effet Sonore : {self.param['cochevolume']}\n")
		f.write(f"Volume Sonore (%) : {self.param['setvolume']}\n")
		f.close()