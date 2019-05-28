import json

class Status():
    # Used when not connected or there is any problem
    ERROR = -1
    # Used when is habitual behavior
    NORMAL = 0
    # Used for activate cheat mission
    CHEAT = 1
    # For say Cheat has ben finished
    CHEAT_FINISHED = 2
    # Stop server connection
    STOP = 255
    # Start Game
    BEGIN = 200

class QueryModel():
    __dictionary__ = {}
    
    def __init__(self, code, turn, actions=None):
        self.__dictionary__["code"] = code
        self.__dictionary__["turn"] = turn
        if actions != None:
            array = []
            for action in actions:
                array.append(action.parseToJson())
            self.__dictionary__["actions"] = array
    
    def parseToJson(self):
        #{"code":"0", "turn":"0", "message": "mensaje de texto"}
        return json.dumps(self.__dictionary__)

    def parseToObject(self, json):
        print("json")

class ResponseModel():
    __code__ = None
    __faceDetection__ = None

    def __init__(self, data):
        dict = json.loads(data)
        print(dict)
        #{ "code":"0", "faceDetection": "0.9"}
        self.__code__ = dict["code"]
        if("faceDetection" in dict):
            self.__faceDetection__ = dict["faceDetection"]
    def getCode(self):
        return self.__code__

    def getFaceDetection(self):
        return self.__faceDetection__
