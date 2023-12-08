from menuEvent import MenuEvent
from premainEvent import PremainEvent
from mainEvent import MainEvent

class FactoryEvent:
    def eventConstructor(self, eventName):
        if eventName == 'Menu':
            return MenuEvent()
        elif eventName == 'preMain':
            return PremainEvent()
        elif eventName == 'Main':
            return MainEvent()
        else:
            raise ValueError(eventName)