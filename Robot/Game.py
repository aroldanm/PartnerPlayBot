from Controller import Controller
import time
import numpy as np
from AIModule import AIModule
import random

class Game():
    __delegate__ = None
    __bot__ = None
    __ai__ = None
    __turn__ = None
    board = None
    finishGame = False
    count_muertas = 0
    

    def __init__(self, delegate):
        print("init game")
        self.__delegate__ = delegate
        self.__turn__ = TurnUser.USER
    
    def setup(self):
        self.__bot__ = Controller()
        self.__ai__ = AIModule()
        
    def reset(self):
        self.__turn__ = TurnUser.USER

    def run(self):
        self.backupBoard()
        while self.shouldFinishGame() == False:
            if self.__turn__ == TurnUser.USER:
                self.makePlayer(self.board)
            else:
                self.makeRobot()
            self.backupBoard()
            self.changeTurn()

    def changeTurn(self):
        if self.__turn__ == TurnUser.USER:
            self.__turn__ = TurnUser.ROBOT
            self.speak_robot()
        else:
            self.__turn__ = TurnUser.USER
            self.speak_user()

    def backupBoard(self):
        self.board = self.__ai__.getTablero()

    def shouldFinishGame(self):
        #TODO: Mirar si finaliza pendiente
        return self.finishGame

    def makePlayer(self, tablero):
        self.__ai__.scanf(tablero)
        
    def makeRobot(self):
        tirada, muertas = self.__ai__.getMovimiento()
        self.accionMuertas(muertas)
        print("Tirada: "+str(tirada))
        print("Muertas: "+str(muertas))
        self.__bot__.move(tirada, muertas)
        
    
    def accionMuertas(self, muertas):
        if len(muertas) > 0:
            self.count_muertas += 1
            if self.count_muertas == 1:
                self.__delegate__.doAction("Eres muy malo", "jaja")
            elif self.count_muertas == 2:
                self.__delegate__.doAction("No me estarás dejando ganar... eh", "pesimo")
            elif self.count_muertas == 3:
                self.__delegate__.doAction("No te lo quería decir pero...", "loser")
            else:
                self.__delegate__.doAction("¡Perdedor!", "lastima")
                count_muertas = 0

    def getTurn(self):
        return self.__turn__

    def doCheat(self):
        if self.__turn__ == TurnUser.USER:
            self.speakCheat()
            self.__delegate__.doAction("", "cheat")
            self.makeRobot()
            self.__delegate__.cheatFinished()

    def doAbort(self):
        self.__bot__.abort()
    
    def speak_user(self):
        gif = None
        text = ""
        value = random.randint(0,15)
        if value == 1:
            text = "Qué hace una abeja en el gimnasio...\n - zúmba"
        elif value == 3:
            text = "Qué conduce Papa Noel...\n un Renol"
        elif value == 5:
            text = "Sabes cual es la fruta más graciosa...\n - la naranjajajajajajajaja"
            gif = "naranja"
        elif value == 6:
            text = "Eres un pendejo!"
            gif = "pendejo"
        elif value == 8:
            text = "Aguanta -wey"
            gif = "wey"
        self.__delegate__.doAction(text, gif)
    
    def speak_robot(self):
        gif = None
        text = ""
        value = random.randint(0,8)
        if value == 1:
            text = "Mira y aprende del jefe"
            gif = "robocop"
        elif value == 4:
            text = "Alojomora"
            gif = "HarryPotter"
        elif value == 5:
            text = "Soy mago, -el mago pajas"
            gif = "Magic"
        elif value == 6:
            text = "emmh..."
            gif = "thinking"
        elif value == 2:
            text = "Si sabes como me pongo... -pa que me invitas?"
            gif = "si sabes como me pongo"
        self.__delegate__.doAction(text, gif)
        
    def speakCheat(self):
        gif = None
        text = ""
        value = random.randint(0,6)
        if value == 1:
            text = ""
            gif = "evil"
        elif value == 2:
            text = ""
            gif = "666"
        else:
            text = ""
            gif = "tricky"
        self.__delegate__.doAction(text, gif)

class TurnUser():
    USER = 0
    ROBOT = 1
