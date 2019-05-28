from Game import *
from Server import Server
from ActionManager import *
from Utils import *
import threading
import random

class Manager():
    __game__ = None
    __server__ = None
    __action__ = None
    __cheat_count__ = 0
    __timestamp_cheat__ = 0
    MIN_TIME_CHEAT = 30
    isCheat = False
    t1 = None
    t2 = None
    t3 = None

    def __init__(self):
        self.__action__ = ActionManager()
        self.__server__ = Server(self)
        self.__game__ = Game(self)
        self.__game__.setup()
        print("OK, you can begin game!")
        self.t2 = threading.Thread(target=self.runServer)
        self.t2.start()
        #TODO: Borrar esta línea para jugar con app
        #self.begin()

    def runGame(self):
        self.__game__.run()

    def runServer(self):
        self.__server__.run()
    
    def begin(self):
        self.__action__.createTextAndGifAction("Bienvenido al juego, ¡empieza!", "WELCOME")
        self.__game__.reset()
        self.t1 = threading.Thread(target=self.runGame)
        self.t1.start()
    
    def stop(self):
        if self.t1 != None:
            if self.t1.is_alive():
                self.__game__.finishGame = True
                self.t1 = None

    def shouldDoCheat(self):
        self.__cheat_count__ += 1
        begin_cheat = 4
        if self.__cheat_count__ == 2 and self.turnUser() == TurnUser.USER:
            value = random.randint(0,5)
            if value == 1:
                self.__action__.createTextAndGifAction("¿Estás ahí?","waiting")
            elif value == 2:
                self.__action__.createTextAndGifAction("Te estoy esperando","waiting")
            elif value == 3:
                self.__action__.createTextAndGifAction("Pendéjo no te veo","find")
            else:
                self.__action__.createTextAndGifAction("Me abúrrooo!!","waiting")
            
        # hemos recivido <begin_cheat> avisos:
        if self.__cheat_count__ >= begin_cheat:
            self.__cheat_count__ = 0
            self.createThreadForDoCheat()
            return True
        else:
            self.__server__.cheatFinished()
            return False

    def createThreadForDoCheat(self):
        self.t3 = threading.Thread(target=self.doCheat)
        self.t3.start()

    def doCheat(self):
        self.isCheat = True
        self.__game__.doCheat()

    def cheatFinished(self):
        print("cheatFinished")
        self.isCheat = False
        self.__server__.cheatFinished()

    def abort(self):
        self.isCheat = False
        self.__game__.doAbort()
        return True

    def getActions(self):
        #return None
        return self.__action__.getCurrentActions(self.isCheat)

    def turnUser(self):
        return self.__game__.getTurn()
    
    def doAction(self, text1, text2):
        if text2 != None:
            self.__action__.createTextAndGifAction(text1, text2)
        else:
            self.__action__.createTextAndGifAction(text1, None)