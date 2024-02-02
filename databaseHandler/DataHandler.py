import jsonpickle
import os
import DataTypes
 
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


class Character:
    def __init__(self, name, id, series, img_urls ="test"):
        self.name = name
        self.id = id
        self.series = series
        self.img_urls = img_urls

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
            f = open(self.__get_player_path(player.user_id), "w")
            f.truncate()
            f.write(jsonpickle.encode(player))
            f.close()





