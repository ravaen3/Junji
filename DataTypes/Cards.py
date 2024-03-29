import discord
import random
import time



class Card:
    def __init__(self, card_id, character_id):
        self.id = card_id
        self.character_id = character_id
        self.options = CardOptions()
    def get_character(self, characters):
        self.character = characters[self.character_id]
        return self.character
class CardOptions:
    def __init__(self):
        self.img = 0

class CardList:
    def __init__(self):
        random.seed(time.time())
        self.available_ids = []
        self.max_id = 1000
        for i in range(1, self.max_id):
            self.available_ids.append(i)
        random.shuffle(self.available_ids)
        self.cards = {}
    def claimCard(self, user_id):
        card = self.available_ids.pop()
        self.available_ids.insert(random.randint(0,len(self.available_ids)),self.max_id)
        self.cards[card] = user_id
        self.max_id+=1
        return card
    def burnCard(self, card_id):
        self.available_ids.append(card_id)

class CardListing:
    def __init__(self, id, owner_id):
        self.id = id
        self.owner_id = owner_id