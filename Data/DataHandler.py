import jsonpickle
import sys, os
import Data.Player
jsp = jsonpickle
class DataHandler:
    def __init__(self, base_path="Data"):
        self.base_path = base_path
        pass
    def is_registered(self,id):
        if os.path.exists(f"{self.base_path}/Players/{id}.json"):
            return True
        else:
            return False
    def register(self, id):
        f = open(f"{self.base_path}/Players/{id}.json", "w")
        f.write(jsp.encode(Data.Player(id)))
        f.close()
    def get_player(self,id):
        f = open(f"{self.base_path}/Players/{id}.json")
        player = jsp.decode(f.read())
        f.close()
        return player
    def save_player(self,player):
        f = open(f"{self.base_path}/Players/{player.user_id}.json", "w")
        f.write(jsp.encode(player))
        f.close()
    def get_characters(self):
        f = open(f"{self.base_path}/Characters/data.json", "r")
        characters = jsp.decode(f.read())
        f.close()
        return characters
    def save_card(self, card):
        card.card_id
        pass



class IDGenData:
    def __init__(self):
        self.free_ids = []
        self.current_id = 0
class IDGen:
    def __init__(self):
        if os.path.exists("Data/IDGenData.json"):
            f = open("Data/IDGenData.json","r")
            self.data = jsp.decode(f.read())
            f.close()
        else:
            self.data = IDGenData()
            self.update()
    def assign_id(self):
        id =self.data.current_id
        self.data.current_id+=1
        self.update()
        return id
    def update(self):
        f = open("Data/IDGenData.json","w")
        f.write(jsp.encode(self.data))
        f.close()
    



