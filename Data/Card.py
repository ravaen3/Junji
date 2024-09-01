import discord
import random
import time
import requests
import Data.DataHandler
from io import BytesIO
from PIL import Image, ImageFont, ImageDraw, ImageOps

dh = Data.DataHandler.DataHandler()
STATS = ["strength","intelligence","charisma","defense","magic_resistance"]
ELEMENTS = ["void","lava","ice","fairy","slime"]

BORDER = Image.open("CardArt\Assets\Border.png")
class Card:
    def __init__(self, character, seed = time.time()):
        self.card_id = None
        self.character=character.get_listing("long")
        self.options = CardOptions()
        self.level = 1
        self.stats = {}
        random.seed(seed)
        self.element = random.choice(ELEMENTS)
        #strength, intelligence, charisma, agility, pr, mr, health, luck
        stat_total = 0
        for stat in STATS:
            self.stats[stat] = random.randint(0,100)
            stat_total+=self.stats[stat]
        self.stats["health"]=100
        self.quality = stat_total/500
        self.owner = None
    def print(self):
        print(f"Character: {self.character} Series: {self.series} Stats: {self.stats} Quality: {self.quality}")
    def getCharacter(self):
        self.character_id

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
        img = Image.new("RGBA", (400, 600))
        img.paste(cardim)
        img.paste(borderc, (0,0),BORDER.convert("RGBA"))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("CardArt\Assets\Fonts\Play-Bold.ttf", 30)
        draw.text((20, 515),f"{character.name}",(0,0,0), font=font)
        font = ImageFont.truetype("CardArt\Assets\Fonts\Play-Bold.ttf", 20)
        draw.text((20, 550),f"{character.series}",(0,0,0), font=font)
        font = ImageFont.truetype("CardArt\Assets\Fonts\Play-Bold.ttf", 30)
        draw.text((260, 540),f"{round(self.quality*100,1)}%",(0,0,0), font=font)
        return img


class CardListing:
    def __init__(self, id, character_listing):
        self.id = id
        self.character = character_listing




class CardOptions:
    def __init__(self):
        self.img = 0
        self.border = ""
        self.font = ""
        self.font_color = ""

#"3hGLn" <- 1. PLAYER INVENTORY 2. Locatable by code 
#"3/hGLn.json"
#!serieslookup Jujutsu
#Select -> Jujutsu Kaisen
#Open and Display -> Data/Series/Jujutsu_Kaisen.csv

#Data/Characters ->
#Data/Series -> JSON file 
#Data/Player -> JSON file for each player
#Data/Cards -> JSON file for each card 3hGLn

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