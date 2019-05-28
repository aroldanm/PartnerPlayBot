from ActionFactory import *
from ActionModel import *
from Utils import *

# Devuelve None si no se puede crear
# Si es posible devolverá un Array de acciones
class ActionManager():
    __factory__ = None
    __actions__ = []
    CLEAR = 20
    __count__ = 0
    
    def __init__(self):
        self.__factory__ = ActionFactory()
    
    def clearActions(self):
        self.__count__ = 0
        self.__actions__ = []
    
    def getTextAction(self, message):
        return self.__factory__.createTextAction(message)

    def getGifAction(self, text):
        return self.__factory__.createGifAction(text)

    def createTextAndGifAction(self, message, text):
        self.clearActions()
        self.__actions__.append(self.getTextAction(message))
        gif = self.getGifAction(text)
        if gif != None:
            self.__actions__.append(gif)

    def getCurrentActions(self, isCheat):
        if self.__actions__ != []:
            if isCheat == True:
                self.__count__ += 1
            else:
                self.__count__ += 2
                
            if self.__count__ > self.CLEAR:
                self.clearActions()
        return self.__actions__

class ActionConfiguration():
    MIN_TIME_MOV = 90
    MIN_TIME_GIF = 30

