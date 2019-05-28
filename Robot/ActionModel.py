import json

class ActionCode():
    # Lanza eventos al movil (gifs, audios, etc)
    REACTION = 0
    # Estado para hacer trampas
    CHEAT = 1
    # Cancelar la acción de trampa
    ABORT = 2

#######################################################

class MoveAction():
    code = None
    timer = 0
    position = None

#######################################################

class ReactionType():
    # Mostrar texto
    TEXT = 0
    # Emitir sonido
    SOUND = 1
    # Mostrar gif
    GIF = 2

class ReactionAction():
    code = None
    type = None
    value = None

    def __init__(self, code, type, value):
        self.code = code
        self.type = type
        self.value = value
    
    def parseToJson(self):
        dictionary = {}
        dictionary["code"] = self.code
        dictionary["type"] = self.type
        dictionary["value"] = self.value
        return json.dumps(dictionary)
