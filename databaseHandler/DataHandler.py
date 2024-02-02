import jsonpickle


class DataHandler():

    def __init__(self, baseDataPath):
        self.basePath = baseDataPath
        f = open(baseDataPath + "/Characters/data.json", "r")
        self.characters = jsonpickle.decode(f.read())
        f.close()
           



    def getCharacter(self,charid):
        return self.characters[charid]
    
    def register(self, playerid):
        if(is_registered(playerid)):
            raise Exception("player is already registered")
        else:
            f = open(self, self.__get_player_path(playerid))
            f.write(jsonpickle.encode(Player(sender_id)))
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
            raise(Exception("player is not registered"))





