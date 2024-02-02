import jsonpickle
import os
import DataTypes

    

class DataHandler():

    def __init__(self, baseDataPath):
        self.basePath = baseDataPath
        f = open(baseDataPath + "/Characters/data.json", "r")
        self.characters = jsonpickle.decode(f.read())
        f.close()
           
    def getCards(self):
        f = open("Cards/data.json", "r")
        cards = jsonpickle.decode(f.read())
        f.close()
        return cards
    
    def getCharacters(self):
        return self.characters
    
    def rewriteCards(self, cards):
        f = open("Cards/data.json", "w")
        f.truncate()
        f.write(jsonpickle.encode(cards))
        f.close()

    def addCard(self, card):
        raise Exception("do not use this yet")
        if(type(card)!= DataTypes.CardListing):
            raise("can not process this datatype as card")
        f = open("Cards/data.json", "r+")
        f.seek(0, os.SEEK_END)
        f.seek(f.tell()-1)
        if f.read(1) != "}":
            raise Exception("error, database aint lookin good")
        f.seek(f.tell()-1)
        f.truncate()
        f.write(",")
        f.write(jsonpickle.encode(card))
        f.write("}")
        f.close()

    def getCharacter(self,charid):
        return self.characters[charid]
    
    def register(self, playerid):
        if(self.is_registered(playerid)):
            raise Exception("player is already registered")
        else:
            f = open(self.__get_player_path(playerid), "w")
            f.write(jsonpickle.encode(Player.Player(playerid)))
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
    
    def modifyPlayer(self, player):
        if(type(player) != DataTypes.Player):
            raise("wrong type specified")
        else:
            f = open(self.__get_player_path(player.id), "w")
            f.truncate()
            f.write(jsonpickle.encode(player))
            f.close()





