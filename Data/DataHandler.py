import jsonpickle
import sys, os
import Data.Player
jsp = jsonpickle
class DataHandler:
    def __init__(self, base_path="Data"):
        self.base_path = base_path
        try:
            open(f"{self.base_path}/Characters/data.json")
        except ValueError:
            raise ValueError(f"Error - Missing {self.base_path}/Characters/data.json file")
        
            
    def is_registered(self,id):
        if os.path.exists(f"{self.base_path}/Players/{id}.json"):
            return True
        else:
            return False
        
    def register(self, id):
        with open(f"{self.base_path}/Players/{id}.json", "w") as f:
            f.write(jsp.encode(Data.Player(id)))
            
    def get_player(self,id):
        return get_json(f"{self.base_path}/Players/{id}.json")
    
    def save_player(self,player):
        with open(f"{self.base_path}/Players/{player.user_id}.json", "w") as f:
            f.write(jsp.encode(player))

    def get_characters(self):
        return get_json(f"{self.base_path}/Characters/data.json")
    def save_card(self, card):
        with open(f"{self.base_path}/Cards/{card.card_id}.json","w") as f:
            f.write(jsp.encode(card))
    
def get_json(path):
    with open(path) as f:
        return jsp.decode(f.read())



class IDGenData:
    def __init__(self):
        self.free_ids = []
        self.current_id = 0
class IDGen:
    def __init__(self):
        if os.path.exists("Data/IDGenData.json"):
            self.data = get_json(f"Data/IDGenData.json")
        else:
            self.data = IDGenData()
            self.update()
    def assign_id(self):
        id =self.data.current_id
        self.data.current_id+=1
        self.update()
        return id
    def update(self):
        with open("Data/IDGenData.json","w") as f:
            f.write(jsp.encode(self.data))
    



