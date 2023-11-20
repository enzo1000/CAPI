#Planoker - Planning Poker
#Created by Aexeos & Zozo, 15/11/2023

import pygame
import numpy as np
from pygame.locals import *
from func_cpe import *
from time import time
from random import random as rdm
import pickle

#INIT DISPLAY
dx, dy = 1600, 900
pygame.init()
ds = pygame.display.set_mode((dx, dy))
pygame.display.set_caption('Planoker')
# pygame.mouse.set_visible(False)
# pygame.display.set_icon(pygame.image.load("picture/icon/icon256.png"))

#IMPORT JOYSTICK

#IMPORT DATA
datafile = 'data/data.ini'

try:
	f = open(datafile, 'rb')
	data = pickle.Unpickler(f).load()
except:
	print('Could\'n open data file')
	print('Create new data.ini ...')
	volume = {'chouquette' : 1}
	data = {'volume' : volume}
set_volume_data(data)

#Coor. Object

#Variable Game

#Variable Loop
game_on = True
mouse = {'action' : 'UP',
		'dy' : {'UP':-120, 'DW':-100},
		'x' : 0, 
		'y' : 0}

activCartes = np.zeros(12).astype(int)

open_event = {'menu' : True,
			'main' : False}

#GAME EVENT
while game_on:

	#MENU EVENT
	while open_event['menu']:
		for event in pygame.event.get():

			if event.type == MOUSEMOTION:

				mouse['x'] = event.pos[0]
				mouse['y'] = event.pos[1]

			if event.type == KEYDOWN:

				if event.key == K_p:
					open_event['menu'], open_event['main'] = False, True

			if event.type == QUIT:
				game_on, open_event['menu'] = False, False

		blitage_menu(ds)


	#MAIN EVENT
	while open_event['main']:
		for event in pygame.event.get():

			if event.type == KEYDOWN:

				if event.key == K_ESCAPE:

					open_event['main'], open_event['menu'] = False, True

			if event.type == MOUSEMOTION:

				mouse['x'] = event.pos[0]
				mouse['y'] = event.pos[1]
				activCartes = motionInCartes(mouse, activCartes)

			if event.type == MOUSEBUTTONDOWN:
				
				select = selectCartes(activCartes)

			if event.type == QUIT:
				game_on, open_event['main'] = False, False

		blitage_main(ds, activCartes)

#EXPORT DATA
f = open(datafile, 'wb')
pickle.Pickler(f).dump(data)