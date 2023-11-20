import pygame
import numpy as np

pygame.init()

#IMPORT
class import_image():
	# CARTES
	folder = "picture/cartes/pngTempo/"
	labelCartes = ['0', '1', '2', '3', '5', '8', '13', '20', '40', '100', 'X', 'Cafe']
	cartes = []

	for label in labelCartes:
		cartes.append(pygame.image.load(f"{folder}carte{label}.png"))

	#MENU IMPORT
	back_menu = pygame.image.load("picture/menu/back_menu.png")

	#MAIN IMPORT
	back_main = pygame.image.load("picture/main/back.png")
	
class import_mixer():
	chouquette = pygame.mixer.Sound("sound/on_chouquette_new.wav")


class import_font():
	font_Karma24 = pygame.font.Font("font/KarmaFuture.ttf", 24)
	font_Karma42 = pygame.font.Font("font/KarmaFuture.ttf", 42)
	font_Karma64 = pygame.font.Font("font/KarmaFuture.ttf", 64)

	font_arial32 = pygame.font.Font("font/arial.ttf", 32)
	font_arial64 = pygame.font.Font("font/arial.ttf", 64)

	font_goodc32 = pygame.font.Font("font/Good Choice.ttf", 32)
	font_goodc48 = pygame.font.Font("font/Good Choice.ttf", 48)
	font_goodc84 = pygame.font.Font("font/Good Choice.ttf", 84)

	# MENU
	title = font_goodc48

class import_data():
	#MAIN DATA
	dimCartes = [200, 300]
	xCartes = np.linspace(200, 1400, 12).astype(int) - int(dimCartes[0]/2)
	yCartes = np.linspace(650, 650, 12).astype(int)  - int(dimCartes[1]/2)
	dxActiv, dyActiv = [0, -200]


class importation():
	image = import_image
	sound = import_mixer
	font = import_font
	data = import_data