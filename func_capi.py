import pygame
from pygame.locals import *
from random import random as rdm
from class_import import importation as impor
import numpy as np

def set_volume_data(data):
	impor.sound.chouquette.set_volume(data['volume']['chouquette'])


def Labelisation(display, font, text, color, X, dX):
	surface = font.render(text, True, color)
	rect = surface.get_rect(center = pygame.Rect(X, dX).center)
	display.blit(surface, rect)


def blitage_main(display, activCartes):
	display.blit(impor.image.back_main, (0, 0))
	Labelisation(display, impor.font.title, "Main", (222, 222, 222), (0, 0), (1600, 100))

	#BLIT CARTES :
	for i, (x, y, activ, carte) in enumerate(zip(impor.data.xCartes, impor.data.yCartes, activCartes, impor.image.cartes)):
		display.blit(carte, (x + activ*impor.data.dxActiv, y + activ*impor.data.dyActiv))

	pygame.display.flip()


def blitage_menu(display):
	display.blit(impor.image.back_menu, (0, 0))
	Labelisation(display, impor.font.title, "Menu", (222, 222, 222), (0, 0), (1600, 100))
	pygame.display.flip()


def motionInCartes(mouse, activCartes):
	for i, (x, y) in enumerate(zip(impor.data.xCartes, impor.data.yCartes)):
		if x < mouse[0] < x + int(impor.data.dimCartes[0]/2) and y < mouse[1] < y + impor.data.dimCartes[1]:
			activCartes[i] = 1
			# print(f"Activ : {impor.image.labelCartes[i]}")
		else:
			activCartes[i] = 0

	return activCartes


def selectCartes(activCartes):
	select = None
	if sum(activCartes) == 1:
		select = impor.image.labelCartes[np.where(activCartes == 1)[0][0]]
		print(f"Activ : {select}")
		
	return select
