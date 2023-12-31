#Plan Poker - Planning Poker
#Created by Aexeos & Zozo, 15/11/2023

from gameClass import GameClass
import factoryEvent as FE

#INIT DISPLAY
#imp = importation()	# SI ON VEUT UTILISER UN SINGLETON ICI


# On créer l'instance GameClass qui va gérer plusieurs paramètre de notre appli (notament la gestion de la fenètre)
game = GameClass((1600, 900), 'Plan Poker', beginBy='menu')

# On créer une instance de chaque Event de notre appli
factory = FE.FactoryEvent()
menu    = factory.eventConstructor('Menu')
premain = factory.eventConstructor('preMain')
main    = factory.eventConstructor('Main')


# Lancement de l'appli !
while game.gameOn:

	# Menu event
	if game.menuOn    : menu.event(game)

	# Pre-main event
	if game.premainOn : premain.event(game)

	# Main event
	if game.mainOn    : main.event(game)

