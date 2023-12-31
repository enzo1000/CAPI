import pygame
import numpy as np
from pygame.locals import *

pygame.init()



class import_image():
	# Sprit des cartes
	folder = "picture/cartes/PNG/"
	labelCartes, cartes = ['0', '1', '2', '3', '5', '8', '13', '20', '40', '100', 'cafe', 'intero'], []
	for label in labelCartes : cartes.append(pygame.image.load(f"{folder}cartes_{label}.png"))

	# Sprit du fond (en commum partout pour l'instant)
	back_main = pygame.image.load("picture/main/back_lum.png")

	# Sprit des bouton
	# - Prefixe "nonon" -> Bouton éteint
	# - Prefixe "activ" -> Bouton allumer
	# - NaN             -> Bouton "inactif" spécial pour les pseudos des joueur en trop
	# - R               -> Bouton en rouge (128) au lieu de gris
	# - G               -> Bouton en vert (128) au lieu de gris
	# - Suffixe Enc     -> Encoche (0 non-coché, 1 coché)
	# - Suffixe Son     -> Icone de son
	sprit_900_80 = (pygame.image.load(f"picture/bouton/nonon-900-80.png"), None)
	sprit_800_400 = (pygame.image.load(f"picture/bouton/nonon-800-400.png"), None)
	sprit_600_100 = (pygame.image.load(f"picture/bouton/nonon-600-100.png"), pygame.image.load(f"picture/bouton/activ-600-100.png"))
	sprit_600_80_Brown = (pygame.image.load(f"picture/bouton/nonon-600-80-Brown.png"), None)
	sprit_480_80 = (pygame.image.load(f"picture/bouton/nonon-480-80.png"), pygame.image.load(f"picture/bouton/activ-480-80.png"))
	sprit_400_80 = (pygame.image.load(f"picture/bouton/nonon-400-80.png"), pygame.image.load(f"picture/bouton/activ-400-80.png"))
	sprit_300_80 = (pygame.image.load(f"picture/bouton/nonon-300-80.png"), pygame.image.load(f"picture/bouton/activ-300-80.png"))
	sprit_300_80_NaN = (pygame.image.load(f"picture/bouton/nonon-300-80-NaN.png"), pygame.image.load(f"picture/bouton/activ-300-80-NaN.png"))
	sprit_240_80_G = (pygame.image.load(f"picture/bouton/nonon-240-80-G.png"), None)
	sprit_160_80 = (pygame.image.load(f"picture/bouton/nonon-160-80.png"),  pygame.image.load(f"picture/bouton/activ-160-80.png"))
	sprit_160_80_R = (pygame.image.load(f"picture/bouton/nonon-160-80-R.png"), pygame.image.load(f"picture/bouton/activ-160-80-R.png"))
	sprit_160_80_G = (pygame.image.load(f"picture/bouton/nonon-160-80-G.png"), pygame.image.load(f"picture/bouton/activ-160-80-G.png"))
	sprit_160_80_Brown = (pygame.image.load(f"picture/bouton/nonon-160-80-Brown.png"), None)
	sprit_160_80_Enc0 = (pygame.image.load(f"picture/bouton/encoche/nonon-160-80_C0.png"), pygame.image.load(f"picture/bouton/encoche/activ-160-80_C0.png"))
	sprit_160_80_Enc1 = (pygame.image.load(f"picture/bouton/encoche/nonon-160-80_C1.png"), pygame.image.load(f"picture/bouton/encoche/activ-160-80_C1.png"))
	sprit_160_80_sonON  = (pygame.image.load(f"picture/bouton/son/nonon-160-80_sonON.png"),  pygame.image.load(f"picture/bouton/son/activ-160-80_sonON.png"))
	sprit_160_80_sonOFF = (pygame.image.load(f"picture/bouton/son/nonon-160-80_sonOFF.png"), pygame.image.load(f"picture/bouton/son/activ-160-80_sonOFF.png"))
	sprit_80_80   = (pygame.image.load(f"picture/bouton/nonon-80-80.png"), None)
	sprit_80_80_R = (pygame.image.load(f"picture/bouton/nonon-80-80-R.png"), None)
	sprit_80_80_G = (pygame.image.load(f"picture/bouton/nonon-80-80-G.png"), None)
	sprit_80_80_K = (pygame.image.load(f"picture/bouton/nonon-80-80-K.png"), None)



class import_color():
	"""
	Importation de couleur
	"""
	rouge = (255, 0  , 0  )
	vert  = (0  , 255, 0  )
	bleu  = (0  , 0  , 255)
	blanc = (255, 255, 255)
	noir  = (0  , 0  , 0  )



class import_mixer():
	"""
	Importation de son
	"""
	try:
		wrong = pygame.mixer.Sound("sound/wrong.mp3")
		carte = pygame.mixer.Sound("sound/bruitCarte.mp3")

		VolumeMaxWrong = 0.2
		VolumeMaxCarte = 0.5
	except:
		print("Audio non initialisé")



class import_font():
	machine48 = pygame.font.Font("font/machine_.ttf", 48)

	arial32 = pygame.font.Font("font/arial.ttf", 32)
	arial64 = pygame.font.Font("font/arial.ttf", 64)

	roboto16 = pygame.font.Font("font/Roboto-Light.ttf", 16)
	roboto32 = pygame.font.Font("font/Roboto-Light.ttf", 32)
	roboto54 = pygame.font.Font("font/Roboto-Light.ttf", 54)

	crash64 = pygame.font.Font("font/Crashnumberingserif.ttf", 64)



class import_data():
	image = import_image
	font = import_font
	color = import_color

	capFPS = 60

	# Association touche / caractère des valeur numérique
	keyValNUM = {K_0:'0',   K_1:'1',   K_2:'2',   K_3:'3',   K_4:'4',   K_5:'5',   K_6:'6',   K_7:'7',   K_8:'8',   K_9:'9', 
			   K_KP0:'0', K_KP1:'1', K_KP2:'2', K_KP3:'3', K_KP4:'4', K_KP5:'5', K_KP6:'6', K_KP7:'7', K_KP8:'8', K_KP9:'9'}

	# Association touche / caractère des valeur alphanum (lower)
	keyVal = {K_a:'a', K_b:'b', K_c:'c', K_d:'d', K_e:'e', K_f:'f', K_g:'g', K_h:'h', K_i:'i', K_j:'j', 
			  K_k:'k', K_l:'l', K_m:'m', K_n:'n', K_o:'o', K_p:'p', K_q:'q', K_r:'r', K_s:'s', K_t:'t', 
			  K_u:'u', K_v:'v', K_w:'w', K_x:'x', K_y:'y', K_z:'z',
			  K_0:'à', K_1:'&', K_2:'é', K_3:'#', K_4:'\'', K_5:'(', K_6:'-', K_7:'è', K_8:'_', K_9:'',
			  K_KP0:'0', K_KP1:'1', K_KP2:'2', K_KP3:'3', K_KP4:'4', K_KP5:'5', K_KP6:'6', K_KP7:'7', K_KP8:'8', K_KP9:'9',
			  K_COMMA:',', K_SEMICOLON:'', K_EXCLAIM:'!', K_RIGHTPAREN:')', K_EQUALS:'=',
			  K_KP_PERIOD:'.', K_KP_MINUS:'-'}

	# Association touche / caractère des valeur alphanum (upper)
	keyValCAP = {K_a:'A', K_b:'B', K_c:'C', K_d:'D', K_e:'E', K_f:'F', K_g:'G', K_h:'H', K_i:'I', K_j:'J', 
			  K_k:'K', K_l:'L', K_m:'M', K_n:'N', K_o:'O', K_p:'P', K_q:'Q', K_r:'R', K_s:'S', K_t:'T', 
			  K_u:'U', K_v:'V', K_w:'W', K_x:'X', K_y:'Y', K_z:'Z',
			  K_0:'0', K_1:'1', K_2:'2', K_3:'3', K_4:'4', K_5:'5', K_6:'6', K_7:'7', K_8:'8', K_9:'9',
			  K_KP0:'0', K_KP1:'1', K_KP2:'2', K_KP3:'3', K_KP4:'4', K_KP5:'5', K_KP6:'6', K_KP7:'7', K_KP8:'8', K_KP9:'9',
			  K_COMMA:'?', K_SEMICOLON:'.', K_EXCLAIM:'§', K_RIGHTPAREN:'°', K_EQUALS:'+',
			  K_KP_PERIOD:'.', K_KP_MINUS:'-'}

	# Association touche / caractère des valeur alphanum (lower & upper) en ajoutant l'espace
	keyValSPACE     = {**keyVal, K_SPACE:' '}
	keyValCAP_SPACE = {**keyValCAP, K_SPACE:' '}


	# MENU DATA
	menu_begin = {'images' : image.sprit_600_100,
		'imgBox' : ((496, 300), (486, 298)),
		'text'   : 'Commencer !',
		'color'  : color.noir,
		'font'   : font.roboto32,
		'box'    : ((500, 300), (600, 100))}

	menu_langue = {'images' : image.sprit_600_100,
		'imgBox' : ((496, 450), (486, 448)),
		'text'   : 'Option',
		'color'  : color.noir,
		'font'   : font.roboto32,
		'box'    : ((500, 450), (600, 100))}

	menu_quit = {'images' : image.sprit_600_100,
		'imgBox' : ((496, 600), (486, 598)),
		'text'   : 'Quitter',
		'color'  : color.noir,
		'font'   : font.roboto32,
		'box'    : ((500, 600), (600, 100))}

	defaultColors = [(64, 64, 64), (0, 0, 0)]
	activColor = (128, 128, 128)


	# MENU DATA : OPTION EVENT
	volume = {'images' : image.sprit_400_80,
		'imgBox'   : ((346, 200), (336, 198)),
		'text'  : 'Effet Sonore :',
		'color' : color.noir,
		'font'  : font.roboto32,
		'box'   : ((350, 200), (400, 80))}
	cocheVolume = {'images' : (*image.sprit_160_80_sonOFF, *image.sprit_160_80_sonON),
		'imgBox' : ((766, 200), (756, 198), (766, 200), (756, 198)),
		'text'   : '',
		'color'  : color.noir,
		'font'   : font.roboto32,
		'box'    : ((770, 200), (160, 80))}
	setVolume = {'images' : image.sprit_300_80,
		'imgBox' : ((946, 200), (936, 198)),
		'text'   : '0x413$Ae',
		'color'  : color.noir,
		'font'   : font.roboto32,
		'box'    : ((950, 200), (300, 80))}

	showFPS = {'images' : image.sprit_400_80,
		'imgBox'   : ((346, 350), (336, 348)),
		'text'  : 'Afficher FPS :',
		'color' : color.noir,
		'font'  : font.roboto32,
		'box'   : ((350, 350), (400, 80))}
	cocheShowFPS = {'images' : (*image.sprit_160_80_Enc0, *image.sprit_160_80_Enc1),
		'imgBox' : ((766, 350), (756, 348), (766, 350), (756, 348)),
		'text'   : '',
		'color'  : color.noir,
		'font'   : font.roboto32,
		'box'    : ((770, 350), (160, 80))}

	capFPSbox = {'images' : image.sprit_400_80,
		'imgBox'   : ((346, 500), (336, 498)),
		'text'  : 'Blocker FPS :',
		'color' : color.noir,
		'font'  : font.roboto32,
		'box'   : ((350, 500), (400, 80))}
	cocheCapFPS = {'images' : (*image.sprit_160_80_Enc0, *image.sprit_160_80_Enc1),
		'imgBox' : ((766, 500), (756, 498), (766, 500), (756, 498)),
		'text'   : '',
		'color'  : color.noir,
		'font'   : font.roboto32,
		'box'    : ((770, 500), (160, 80))}

	validerOption = {'images' : (*image.sprit_160_80, *image.sprit_160_80_R),
		'imgBox': ((716, 750), (706, 748), (716, 750), (706, 748)),
		'text'  : 'Menu',
		'color' : color.noir,
		'font'  : font.roboto32,
		'box'   : ((720, 750), (160, 80))}


	# PRE-MAIN DATA
	player = {'images' : image.sprit_400_80,
		'imgBox'   : ((346, 150), (336, 148)),
		'text'  : 'Nombre de joueur :',
		'color' : color.noir,
		'font'  : font.roboto32,
		'box'   : ((350, 150), (400, 80))}
	nbPlayer = {'images' : image.sprit_160_80,
		'imgBox' : ((766, 150), (756, 148)),
		'text'   : '0x413$Ae', # 0x413$Ae est mon code palceholder car ici le texte est variable, donc donner ulterirement : si il s'affiche c'est que l'on a oublier un truc
		'color'  : color.noir,
		'font'   : font.roboto32,
		'box'    : ((770, 150), (160, 80))}
	setName = {'images' : image.sprit_300_80,
		'imgBox' : ((946, 150), (936, 148)),
		'text'   : 'Liste Noms',
		'color'  : color.noir,
		'font'   : font.roboto32,
		'box'    : ((950, 150), (300, 80))}

	backlog = {'images' : image.sprit_400_80,
		'imgBox': ((346, 300), (336, 298)),
		'text'  : 'Choix Backlog :',
		'color' : color.noir,
		'font'  : font.roboto32,
		'box'   : ((350, 300), (400, 80))}
	setBacklog = {'images' : image.sprit_480_80,
		'imgBox': ((766, 300), (756, 298)),
		'text'  : '0x413$Ae',
		'color' : color.noir,
		'font'  : font.roboto32,
		'box'   : ((770, 300), (480, 80))}

	mode = {'images' : image.sprit_400_80,
		'imgBox': ((346, 450), (336, 448)),
		'text'  : 'Choix Mode :',
		'color' : color.noir,
		'font'  : font.roboto32,
		'box'   : ((350, 450), (400, 80))}
	setMode = {'images' : image.sprit_480_80,
		'imgBox': ((766, 450), (756, 448)),
		'text'  : '0x413$Ae',
		'color' : color.noir,
		'font'  : font.roboto32,
		'box'   : ((770, 450), (480, 80))}

	chrono = {'images' : image.sprit_400_80,
		'imgBox'   : ((346, 600), (336, 598)),
		'text'  : 'Jouer avec Chrono :',
		'color' : color.noir,
		'font'  : font.roboto32,
		'box'   : ((350, 600), (400, 80))}
	cocheChrono = {'images' : (*image.sprit_160_80_Enc0, *image.sprit_160_80_Enc1),
		'imgBox' : ((766, 600), (756, 598), (766, 600), (756, 598)),
		'text'   : '',
		'color'  : color.noir,
		'font'   : font.roboto32,
		'box'    : ((770, 600), (160, 80))}
	setChrono = {'images' : image.sprit_300_80,
		'imgBox' : ((946, 600), (936, 598)),
		'text'   : '0x413$Ae',
		'color'  : color.noir,
		'font'   : font.roboto32,
		'box'    : ((950, 600), (300, 80))}

	lezgo = {'images' : (*image.sprit_160_80, *image.sprit_160_80_R),
		'imgBox': ((716, 750), (706, 748), (716, 750), (706, 748)),
		'text'  : 'Let\'s go !',
		'color' : color.noir,
		'font'  : font.roboto32,
		'box'   : ((720, 750), (160, 80))}


	# PRE-MAIN DATA : SET NB PLAYER
	minPlayer = 2
	maxPlayer = 10
	confirmNb = {'images' : image.sprit_160_80_G,
		'imgBox': ((896, 750), (886, 748)),
		'text'  : 'Valider',
		'color' : color.noir,
		'font'  : font.roboto32,
		'box'   : ((900, 750), (160, 80))}


	# PRE_MAIN DATA : SET PLAYER NAME
	limitPseudo = 14
	listName = {'images' : (*image.sprit_300_80, *image.sprit_300_80_NaN),
		'imgBox': [((442+408*(i%2), 250+100*(i//2)), (432+408*(i%2), 248+100*(i//2)), (442+408*(i%2), 250+100*(i//2)), (432+408*(i%2), 248+100*(i//2))) for i in range(10)],
		'text'  : '0x413$Ae',
		'color' : color.noir,
		'font'  : font.roboto32,
		'box'   : [((446+408*(i%2), 250+100*(i//2)), (300, 80)) for i in range(10)]}
	confirmName = {'images' : image.sprit_160_80_G,
		'imgBox': ((896, 750), (886, 748)),
		'text'  : 'Valider',
		'color' : color.noir,
		'font'  : font.roboto32,
		'box'   : ((900, 750), (160, 80))}
	retour = {'images' : (*image.sprit_160_80, *image.sprit_160_80_R),
		'imgBox': ((716, 750), (706, 748), (716, 750), (706, 748)),
		'text'  : 'Retour',
		'color' : color.noir,
		'font'  : font.roboto32,
		'box'   : ((720, 750), (160, 80))}


	# PRE-MAIN DATA : SET BACKLOG EVENT
	# ****


	# PRE-MAIN DATA : ERASE BACKLOG EVENT
	eraseQuestion = {'images' : image.sprit_800_400,
		'imgBox': ((396, 200), None),
		'text'  : 'Le Backlog selectioné est déjà entièrement compléter,',
		'color' : color.noir,
		'font'  : font.roboto32,
		'box'   : ((400, 200), (800, 400))}
	eraseOui = {'images' : image.sprit_160_80,
		'imgBox': ((446, 700), (436, 700)),
		'text'  : 'Oui !',
		'color' : color.noir,
		'font'  : font.roboto32,
		'box'   : ((450, 700), (160, 80))}
	eraseNon = {'images' : image.sprit_160_80,
		'imgBox': ((986, 700), (976, 700)),
		'text'  : 'Non ?!',
		'color' : color.noir,
		'font'  : font.roboto32,
		'box'   : ((990, 700), (160, 80))}


	# PRE-MAIN DATA : SET MODE EVENT
	listMode = {'images' : image.sprit_480_80,
		'imgBox': [((556, 250+100*i), (546, 248+100*i)) for i in range(5)],
		'text'  : ['Unanimité', 'Moyenne', 'Mediane', 'Majorité Abso.', 'Majorité rela.'],
		'color' : color.noir,
		'font'  : font.roboto32,
		'box'   : [((560, 250+100*i), (480, 80)) for i in range(5)]}


	# PRE-MAIN DATA : SET CHRONO
	minTimeChrono = 10  # sec
	maxTimeChrono = 300 # sec


	# MAIN DATA
	dimCartes = [200, 300]
	xCartes = np.linspace(200, 1400, 12).astype(int) - int(dimCartes[0]/2)
	yCartes = np.linspace(650, 650, 12).astype(int)  - int(dimCartes[1]/2)
	dxActiv, dyActiv = [0, -200]

	currentTime = {'images' : image.sprit_160_80,
		'imgBox': ((36, 41), (None, None)),
		'text'  : '0x413$Ae',
		'color' : color.noir,
		'font'  : font.machine48,
		'box'   : ((44, 45), (160, 80))}

	task = {'images' : image.sprit_160_80,
		'imgBox': ((36, 200), (None, None)),
		'text'  : 'Tache :',
		'color' : color.noir,
		'font'  : font.roboto32,
		'box'   : ((40, 200), (160, 80))}
	currentTask = {'images' : image.sprit_900_80,
		'imgBox': ((212, 200), (None, None)),
		'text'  : '0x413$Ae',
		'color' : color.noir,
		'font'  : font.roboto32,
		'box'   : ((216, 200), (900, 80))}
	mainPlayer = {'images' : image.sprit_160_80,
		'imgBox': ((36, 296), (None, None)),
		'text'  : 'Joueur :',
		'color' : color.noir,
		'font'  : font.roboto32,
		'box'   : ((40, 296), (160, 80))}
	currentMainPlayer = {'images' : image.sprit_300_80,
		'imgBox': ((212, 296), (None, None)),
		'text'  : '0x413$Ae',
		'color' : color.noir,
		'font'  : font.roboto32,
		'box'   : ((216, 296), (300, 80))}


	# MAIN DATA : END TASK EVENT
	finalValue = {'images' : image.sprit_240_80_G,
		'imgBox': ((591, 150), (581, 148)),
		'text'  : '0x413$Ae',
		'color' : color.noir,
		'font'  : font.roboto32,
		'box'   : ((599, 150), (240, 80))}
	caseValue  = {'images' : image.sprit_80_80_G,
		'imgBox': ((841, 150), (831, 148)),
		'text'  : '0x413$Ae',
		'color' : color.noir,
		'font'  : font.roboto32,
		'box'   : ((845, 150), (80, 80))}
	listVotes = {'images' : image.sprit_300_80,
		'imgBox': [((346+500*(i%2), 250+100*(i//2)), None) for i in range(10)],
		'text'  : '0x413$Ae',
		'color' : color.noir,
		'font'  : font.roboto32,
		'box'   : [((354+500*(i%2), 250+100*(i//2)), (300, 80)) for i in range(10)]}
	caseVotes = {'images' : (image.sprit_80_80[0], image.sprit_80_80_G[0], image.sprit_80_80_R[0], image.sprit_80_80_K[0]),
		'imgBox': [((656+500*(i%2), 250+100*(i//2)), None) for i in range(10)],
		'text'  : '0x413$Ae',
		'color' : color.noir,
		'font'  : font.roboto32,
		'box'   : [((664+500*(i%2), 250+100*(i//2)), (80, 80)) for i in range(10)]}
	nextBox = {'images' : image.sprit_300_80,
		'imgBox': ((646, 750), (636, 748)),
		'text'  : '0x413$Ae',
		'color' : color.noir,
		'font'  : font.roboto32,
		'box'   : ((650, 750), (300, 80))}


	# MAIN DATA : EXPLICATION EVENT
	limitExplication = 240
	explicationRL = 38
	explicationFontSize = 32
	explication = {'images' : image.sprit_800_400,
		'imgBox': ((396, 200), None),
		'text'  : '0x413$Ae',
		'color' : color.noir,
		'font'  : font.arial32,
		'box'   : ((400, 200), (800, 400))}


	# MAIN DATA : CAFE EVENT
	fin = {'images' : image.sprit_300_80,
		'imgBox': ((646, 750), (636, 748)),
		'text'  : 'Sauvegarde Backlog',
		'color' : color.noir,
		'font'  : font.roboto32,
		'box'   : ((650, 750), (300, 80))}


#Singleton
def singleton(class_):
	instances = {}
	def getinstance(*args, **kwargs):
		if class_ not in instances:
			instances[class_] = class_(*args, **kwargs)
		return instances[class_]
	return getinstance


@singleton
class importation():
	image = import_image
	color = import_color
	sound = import_mixer
	font = import_font
	data = import_data
