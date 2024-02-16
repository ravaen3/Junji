import jsonpickle
import os
import DataTypes
import re
class DataHandler():

    def __init__(self, baseDataPath):
        self.basePath = baseDataPath
        f = open(baseDataPath + "/Characters/data.json", "r")
        self.characters = jsonpickle.decode(f.read())
        f.close()
           
    def getCards(self, character_id):
        if os.path.exists(f"Cards/{character_id}.json"):
            f = open(f"Cards/{character_id}.json", "r")
            cards = jsonpickle.decode(f.read())
            f.close()
            return cards
        else:
            return DataTypes.Cards.CardList()

    def getCharacters(self):
        return self.characters
    
    def rewriteCards(self, cards, character_id):
        f = open(f"Cards/{character_id}.json", "w")
        f.truncate()
        f.write(jsonpickle.encode(cards))
        f.close()



    def getCharacter(self,charid):
        return self.characters[charid]
    
    def register(self, playerid):
        if(self.is_registered(playerid)):
            raise Exception("player is already registered")
        else:
            f = open(self.__get_player_path(playerid), "w")
            f.write(jsonpickle.encode(DataTypes.Player(playerid)))
            f.close()
    
    def __get_player_path(self, playerid):
        return self.basePath + "/Players/" + str(playerid) + ".json"
    
    def is_registered(self, playerid):
            if isinstance(playerid, str):
                playerid = int(re.search(r"\d+", playerid).group())
            if(os.path.exists(self.__get_player_path(playerid))):
                return True
            else:
                return False
    
    def getPlayer(self, playerid):
        if isinstance(playerid, str):
                playerid = int(re.search(r"\d+", playerid).group())
        if(self.is_registered(playerid)):
            f = open(self.__get_player_path(playerid))
            player = jsonpickle.decode(f.read())
            f.close()
            return player
        else:
            raise(Exception(f"player {playerid} is not registered"))
    
    def modifyPlayer(self, player):
        if(type(player) != DataTypes.Player):
            raise("wrong type specified")
        else:
            f = open(self.__get_player_path(player.user_id), "w")
            f.truncate()
            f.write(jsonpickle.encode(player))
            f.close()





