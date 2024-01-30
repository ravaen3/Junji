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
import threading
import sys

load_dotenv()
sqids = Sqids(alphabet="kEjqW4T673ePsJNoACFwUVy1Ofabmz5nxGDtcHZQ2lpgrSLdhM0uR8iKIvBX9Y", min_length=4)

class BotData(object):
    pass
class Character:
    def __init__(self, name, series, img_url ="test"):
        self.name = name
        self.series = series
        self.img_url = img_url
    def print(self):
        print(f"name={self.name}")
        print(f"series={self.series}")
        print(f"img_url={self.img_url}")
    def sendAsMessage(self, channel):
        mstring = f"{self.name} from {self.series} has dropped."
        channel.send(mstring, embeds=discord.Embed.from_dict({ "url" : self.img_url}))
        


class Card:
    def __init__(self, id, character):
        self.id = sqids.encode(id)
        self.character = character

class Player:
    def __init__(self, user_id):
        self.user_id = user_id
        self.curreny = 0
        self.max_rolls = 20
        self.max_grabs = 1
        self.last_roll_time = 0
        self.last_grab_time = 0
        self.cards = []
        self.upgrades = []
        self.inventory = []
    
def load_data():
    f = open("data.json")
    botdata = jsonpickle.decode(f.read())
    f.close()

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
    print(bot.user.id)

@bot.command(aliases=["r"])
async def register(ctx):
    sender_id = ctx.author.id
    is_registered = os.path.exists("Players/"+str(sender_id)+".json")
    if is_registered:
        await ctx.channel.send("You are already registered!")
    else:
        f = open("Players/"+str(sender_id), "w")
        f.write(jsonpickle.encode(Player(sender_id)))
        f.close()
        await ctx.channel.send("You have registered successfully!")
        


#bot.run('MTAwNjkwODA3MjQ5NDYzNzA3Ng.G3D-72.cJBtxEnMHni9K8LkgoKtHO0BkzSMBDMTJIlmZQ')
print("testtetsestestestestse")
generate_card_drop().print()

if(len(sys.argv)>=2 and sys.argv[1]=='run'):
    bot.run(base64.b64decode(os.getenv('TOKEN').encode("utf-8")).decode("utf-8"))

#botthread = threading.Thread(target=bot.run, args=(base64.b64decode(os.getenv('TOKEN').encode("utf-8")).decode("utf-8") ,))
#botthread.start()
#botthread.join()