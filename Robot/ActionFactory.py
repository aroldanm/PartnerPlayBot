from ActionModel import *

class ActionFactory():

    def createTextAction(self, message):
        return ReactionAction(ActionCode.REACTION, ReactionType.TEXT, message)

    def createGifAction(self, text):
        return ReactionAction(ActionCode.REACTION, ReactionType.GIF, text)
    
    @staticmethod
    def create(code, object=None):
        if code == ActionCode.REACTION:
            #Se le debe pasar en Object uno de tipo 'ReactionAction'
            if object != None:
                #TODO: Revisar
                reaction = ReactionAction()
                reaction.code = object.code
                reaction.reaction = object
            return None
        
        elif code == ActionCode.CHEAT:
            if object != None:
                #TODO: Revisar
                moveAction = MoveAction()
                moveAction.timer = 0.03
                moveAction.position = object
                return moveAction
            return None
        
        else: #ABORT
            #TODO: Revisar
            moveAction = MoveAction()
            moveAction.timer = 0.015
            moveAction.position = "INIT"
            return moveAction
