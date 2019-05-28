import socket
import time
from Model import *

class Server():
    __delegate__ = None
    socket = None
    status = Status.ERROR
    timeInterval = 1

    def __init__(self, delegate):
        self.__delegate__ = delegate
        print("init server")

    def run(self):
        self.socket = socket.socket()

        # Prevent socket.error: [Errno 98] Address already in use
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.socket.bind(("172.20.10.7", 9876))
        #self.socket.bind(("192.168.0.26", 9876))
        self.socket.listen(1)

        print("Waiting client connection...")
        c, addr = self.socket.accept()
        print("Connected with " + addr[0])
        self.status = Status.NORMAL
        
        begin = 0
        while begin != Status.BEGIN and begin != Status.STOP :
           response = self.waitResponse(c.recv(1024))
           begin = self.processResponse(response)
        if begin == Status.BEGIN:
            print("Begin game")
            self.beginGame()
            while True:
                time.sleep(self.timeInterval)
                try:
                    smessage = self.processQuery(self.status)
                    c.send(smessage.encode())
                
                    response = self.waitResponse(c.recv(1024))
                    code = self.processResponse(response)
                
                    if(code == Status.STOP):
                        break
                except socket.error:
                    print("Error socket comunication")
                    break
        c.close()
        print("Connection closed")
        self.stopGame()
        self.run()
                
    def waitResponse(self, data):
        response = data.decode('utf-8')
        return response.replace("\r\n", '')

    def processQuery(self, status):
        turn = self.__delegate__.turnUser()
        actions = self.__delegate__.getActions()
        query = QueryModel(status, turn, actions)
        return query.parseToJson()
        
    def processResponse(self, data):
        model = ResponseModel(data)
        code = int(model.getCode())
        
        if(code == Status.BEGIN or code == Status.STOP):
            return code
        else:
            faceDetection = float(model.getFaceDetection())
            
            if(self.status == Status.CHEAT_FINISHED):
                self.status = Status.NORMAL
                self.timeInterval = 1
            elif(code == Status.CHEAT):
                # Face detected
                if(faceDetection > 0.01):
                    if self.processAbortCheatMission():
                        self.status = Status.NORMAL
                        self.timeInterval = 1
            elif(code == Status.NORMAL):
                # Face hasn't been detected
                if(faceDetection == 0):
                    if self.becomeCheatMission():
                        self.status = Status.CHEAT
                        self.timeInterval = 0.2
            return code
    
    def becomeCheatMission(self):
        return self.__delegate__.shouldDoCheat()
    
    def processAbortCheatMission(self):
        return self.__delegate__.abort()
    
    def cheatFinished(self):
        self.status = Status.CHEAT_FINISHED

    def beginGame(self):
        self.__delegate__.begin()

    def stopGame(self):
        self.__delegate__.stop()
