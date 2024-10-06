import time
import Data.DataHandler
dh = Data.DataHandler.DataHandler()
class Inventory:
    def __init__(self):
        #Cards
        self.cards = []
        #Cosmetics
        self.arts = []
        self.borders = []
        self.fonts = []
        #Equipment
        self.weapons = []
        self.armors = []
        self.moves = []

class Player:
    def __init__(self, user_id):
        self.user_id = user_id
        self.account_types = ["user"] #user, admin, mod,
        self.coins=0
        self.gems=0
        self.inventory = Inventory()
        self.wishlist = []
        self.upgrades = []

        self.last_grab_time = 0
        self.drops = 3
        self.last_drop_time = 0

    def save(self):
        print(self)
        dh.save_player(self)
    def claim(self, card):
        self.inventory.cards.append(card)
    def drop():
        pass







                #cards = sorted(cards, key=lambda x: x.character.series[0])
