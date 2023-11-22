#Plan Poker - Planning Poker
#Created by Aexeos & Zozo, 15/11/2023

from gameClass import GameClass
from menuEvent import MenuEvent
from premainEvent import PremainEvent
from mainEvent import MainEvent

#INIT DISPLAY
#imp = importation()	# SI ON VEUT UTILISER UN SINGLETON ICI

game = GameClass((1600, 900), 'Plan Poker')
game.menuOn = True

menu    = MenuEvent()
premain = PremainEvent()
main    = MainEvent()


#GAME EVENT
while game.gameOn:

	# Menu event
	if game.menuOn    : menu.event(game)

	# Pre-main event
	if game.premainOn : premain.event(game)

	# Main event
	if game.mainOn    : main.event(game)

