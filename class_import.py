import pygame
import numpy as np

pygame.init()

#IMPORT
#TODO : CHANGER CE FICHIER EN UNE GRANDE CLASSE AVEC PLUSIEURS FONCTIONS POUR IMPORTER LES ELEMENTS
# C'EST LORS DE LA CREATION / INITIALISATION DE LA CLASSE QUE LES IMPORT SE REALISERON
# ON PEUT AUSSI IMAGINER UN SINGLETON PATTERN ICI

class import_image():
	# CARTES
	folder = "picture/cartes/pngTempo/"
	labelCartes = ['0', '1', '2', '3', '5', '8', '13', '20', '40', '100', 'X', 'Cafe']
	cartes = []

	for label in labelCartes:
		cartes.append(pygame.image.load(f"{folder}carte{label}.png"))

	# MENU IMPORT
	back_menu = pygame.image.load("picture/menu/back_menu.png")

	# PRE-MAIN IMPORT
	coche = [pygame.image.load("picture/pre_main/cocheOff.png"), pygame.image.load("picture/pre_main/cocheOn.png")]

	# MAIN IMPORT
	back_main = pygame.image.load("picture/main/back.png")
	
class import_mixer():
	chouquette = pygame.mixer.Sound("sound/on_chouquette_new.wav")


class import_font():
	font_Karma64 = pygame.font.Font("font/KarmaFuture.ttf", 64)

	font_arial32 = pygame.font.Font("font/arial.ttf", 32)
	font_arial64 = pygame.font.Font("font/arial.ttf", 64)

	font_goodc32 = pygame.font.Font("font/Good Choice.ttf", 32)
	font_goodc48 = pygame.font.Font("font/Good Choice.ttf", 48)
	font_goodc84 = pygame.font.Font("font/Good Choice.ttf", 84)

	font_roboto16 = pygame.font.Font("font/Roboto-Light.ttf", 16)
	font_roboto32 = pygame.font.Font("font/Roboto-Light.ttf", 32)
	font_roboto54 = pygame.font.Font("font/Roboto-Light.ttf", 54)

	placeholder = font_Karma64

	# EVENT
	fps = font_roboto16

	# MENU
	menu_title  = font_roboto54
	menu_choice = font_roboto32

	# MAIN
	task = font_arial32
	player = font_arial32

class import_data():
	# DISPLAY DATA
	displayWindowsSize = (1600, 900)

	# MENU DATA
	defaultColors = [(64, 64, 64), (0, 0, 0)]
	activColor = (128, 128, 128)
	Mbg_Box = ((500, 300), (600, 100))
	Mlg_Box = ((500, 450), (600, 100))
	Mqt_Box = ((500, 600), (600, 100))

	# PRE-MAIN DATA
	PMnp_Box   = ((350, 300), (400, 80))
	PMnpnb_Box = ((770, 300), (160, 80))
	PMnpsn_Box = ((950, 300), (300, 80))

	PMbl_Box   = ((350, 450), (400, 80))
	PMblsn_Box = ((770, 450), (480, 80))

	PMmd_Box   = ((350, 600), (400, 80))
	PMmdch_Box = ((770, 600), (480, 80))

	PMlg_Box = ((700, 750), (200, 80))


	# PRE-MAIN DATA : SET BACKLOG EVENT
	PMSBback_Box = ((350, 200), (900, 670))
	testBacklog  = {'BacklogTest0' : [{'Tache 1' : -1, 'Tache 2' :  1, 'Tache 3' :  3}, [2, 1, 3]],
				    'BacklogTest1' : [{'Tache 7' : -1, 'Tache 8' : -1, 'Tache 9' : -1}, [0, 3, 3]]}
	listBacklog  = list(testBacklog.keys())
	PMSBlist_Box = [((500, 250 + 100*i), (490, 90)) for i in range(len(listBacklog))]
	PMSBscor_Box = [((1000, 250 + 100*i), (100, 90)) for i in range(len(listBacklog))]

	# PRE-MAIN DATA : SET MODE EVENT
	PMSMback_Box = ((350, 200), (900, 670))
	listMode     = ['Unanimité', 'Moyenne', 'Mediane', 'Majorité Abso.', 'Majorité rela.']
	PMSMlist_Box = [((550, 250 + 100*i), (500, 90)) for i in range(len(listMode))]

	#MAIN DATA
	dimCartes = [200, 300]
	xCartes = np.linspace(200, 1400, 12).astype(int) - int(dimCartes[0]/2)
	yCartes = np.linspace(650, 650, 12).astype(int)  - int(dimCartes[1]/2)
	dxActiv, dyActiv = [0, -200]

#SI ON VEUT UTILISER UN SINGLETON (changement ici et dans main capi)
# def singleton(class_):
#     instances = {}
#     def getinstance(*args, **kwargs):
#         if class_ not in instances:
#             instances[class_] = class_(*args, **kwargs)
#         return instances[class_]
#     return getinstance

#@singleton
class importation():
	image = import_image
	sound = import_mixer
	font = import_font
	data = import_data

