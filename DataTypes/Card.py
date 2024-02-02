import discord

class Card:
    def __init__(self, id, character):
        self.id = id
        self.character = character
        self.options = CardOptions()
    async def sendAsCard(self, channel):
        name = self.character.name.replace("_"," ")


class CardOptions:
    def __init__(self):
        self.img = 0

class CardListing:
    def __init__(self, id, owner_id):
        self.id = id
        self.owner_id = owner_id