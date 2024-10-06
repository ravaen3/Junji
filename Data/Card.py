import discord
import random
import time
import requests
import Data.DataHandler
from io import BytesIO
from PIL import Image, ImageFont, ImageDraw, ImageOps

dh = Data.DataHandler.DataHandler()
idg = Data.DataHandler.IDGen()
STATS = ("strength","intelligence","speed","defense","magic_resistance")
ELEMENTS = ("void","lava","ice","fairy","slime")

BORDER = Image.open("CardArt\Assets\Border.png")
class Card:
    def __init__(self, character, seed = time.time()):
        #Card Information
        self.card_id = None
        self.type = "normal"
        self.character=character.get_listing("long")
        self.owner_id = None
        self.history = []

        #Customisation
        self.options = CardOptions() #Cosmetic

        #Battle
        self.level = 1
        self.stats = {}
        random.seed(seed)
        self.element = random.choice(ELEMENTS)
        stat_total = 0
        for stat in STATS:
            self.stats[stat] = random.randint(0,100)
            stat_total+=self.stats[stat]
        self.stats["health"]=100
        self.quality = stat_total/500

    def print(self):
        print(f"Character: {self.character} Series: {self.series} Stats: {self.stats} Quality: {self.quality}")

    def set_owner(self, player):
        self.owner_id = player.user_id
        self.history.append([self.owner_id, time.time()])
    def claim_id(self):
        self.card_id = idg.assign_id()
    def claim(self):
        pass
    def save(self):
        dh.save_card(self)
    def fuse(self, card):
        pass
    def image(self):
        character = self.character
        color = "white"
        match self.element:
            case "void":
                color = "purple"
            case "lava":
                color = "red"
            case "ice":
                color = "#0096FF"
            case "fairy":
                color = "#FF80FF"
            case "slime":
                color = "lime"
        borderc = ImageOps.colorize(ImageOps.grayscale(BORDER), black="black",white=color)
        print(character.art_urls)
        response = requests.get(character.art_urls["0"])
        cardim = Image.open(BytesIO(response.content))
        cardim=ImageOps.fit(cardim,(400, 600))
        img = Image.new("RGBA", (400, 600))
        img.paste(cardim)
        img.paste(borderc, (0,0),BORDER.convert("RGBA"))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("CardArt\Assets\Fonts\Play-Bold.ttf", 30)
        draw.text((20, 515),f"{character.name}",(0,0,0), font=font)
        font = ImageFont.truetype("CardArt\Assets\Fonts\Play-Bold.ttf", 20)
        draw.text((20, 550),f"{character.series[0]}",(0,0,0), font=font)
        font = ImageFont.truetype("CardArt\Assets\Fonts\Play-Bold.ttf", 30)
        draw.text((260, 540),f"{round(self.quality*100,1)}%",(0,0,0), font=font)
        return img


class CardListing:
    def __init__(self, id, character_listing):
        self.id = id
        self.character = character_listing




class CardOptions:
    def __init__(self):
        #Cosmetic
        self.img = 0
        self.border = ""
        self.font = ""
        self.font_color = ""
        #Battle
        self.equipment = [None,None,None,None] #Head, Torso, Legs, Weapon
        self.moves = []

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