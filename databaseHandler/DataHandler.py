import jsonpickle
import os

class Player:
    def __init__(self, user_id):
        self.user_id = user_id
        self.curreny = 0
        self.rolls = 20
        self.grabs = 1
        self.max_rolls = 10
        self.max_grabs = 2
        self.last_roll_time = 0
        self.last_grab_time = 0
        self.cards = []
        self.upgrades = []
        self.inventory = []

    

class DataHandler():

    def __init__(self, baseDataPath):
        self.basePath = baseDataPath
        f = open(baseDataPath + "/Characters/data.json", "r")
        self.characters = jsonpickle.decode(f.read())
        f.close()
           



    def getCharacter(self,charid):
        return self.characters[charid]
    
    def register(self, playerid):
        if(self.is_registered(playerid)):
            raise Exception("player is already registered")
        else:
            f = open(self.__get_player_path(playerid), "w")
            f.write(jsonpickle.encode(Player(playerid)))
            f.close()
    
    def __get_player_path(self, playerid):
        return self.basePath + "/Players/" + str(playerid) + ".json"
    
    def is_registered(self, playerid):
            if(os.path.exists(self.__get_player_path(playerid))):
                return True
            else:
                return False
    
    def getPlayer(self, playerid):
        if(self.is_registered(playerid)):
            f = open(self.__get_player_path(playerid))
            player = jsonpickle.decode(f.read())
            f.close()
            return player
        else:
            raise(Exception(f"player {playerid} is not registered"))





