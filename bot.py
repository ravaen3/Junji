from asyncio.windows_events import NULL
import random
from tracemalloc import start
import jsonpickle
import discord
from discord.ext import commands
import time
import os
from sqids import Sqids
from dotenv import load_dotenv
import base64


load_dotenv()
sqids = Sqids(alphabet="kEjqW4T673ePsJNoACFwUVy1Ofabmz5nxGDtcHZQ2lpgrSLdhM0uR8iKIvBX9Y", min_length=6)

class BotData(object):
    pass
class Character:
    def __init__(self, name, series, img_url ="test"):
        self.name = name
        self.series = series
        self.img_url = img_url

class Card:
    def __init__(self, id, character):
        self.id = sqids.encode(id)
        self.character = character
class Player:
    def __init__(self, ):
        pass
    
def load_data():
    f = open("data.json")
    botdata = jsonpickle.decode(f.read())
    f.close()
    print(botdata.current_id)

def load_characters():
    f = open("Characters\data.json", "r")
    data = jsonpickle.decode(f.read())
    f.close()
    return data
def generate_card_drop():
    random.seed(time.time())
    drop = random.choice(list(characters.values()))
    return drop
def load_card():
    pass
characters = load_characters()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!",intents=intents)
@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
@bot.command(aliases=["r"])
async def register(ctx):
    sender_id = ctx.author.id
    is_registered = os.path.exists("Players/"+sender_id)
    if is_registered:
        print("You are already registered!")
    else:
        f = open("Players/"+str(sender_id), "w")
        f.write()
        
bot.run(base64.b64decode(os.getenv('TOKEN').encode("utf-8")).decode("utf-8"))
#bot.run('MTAwNjkwODA3MjQ5NDYzNzA3Ng.G3D-72.cJBtxEnMHni9K8LkgoKtHO0BkzSMBDMTJIlmZQ')
load_data()
print(generate_card_drop())