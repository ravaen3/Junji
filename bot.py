from asyncio.windows_events import NULL
import asyncio
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
    async def sendAsMessage(self, channel):
        name = self.name.replace("_"," ")
        mstring = f"{name} from {self.series} has dropped."
        embedVar = discord.Embed(title=self.name, description=self.series, color=0x00ff00, url=self.img_url)
        embedVar.set_image(url=self.img_url)
        button = discord.ui.Button(style=discord.ButtonStyle.danger, label="test")
        view1 = discord.ui.View(timeout= 60.0)
        view1.add_item(button)
        await channel.send(content=mstring, embed=embedVar, view=view1)
        


class Card:
    def __init__(self, id, character):
        self.id = sqids.encode(id)
        self.character = character

class Player:
    def __init__(self, user_id):
        self.user_id = user_id
        self.curreny = 0
        self.rolls = 20
        self.grabs = 1
        self.max_rolls = 10
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
    f = open("Characters\\data.json", "r")
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
        f = open("Players/"+str(sender_id)+".json", "w")
        f.write(jsonpickle.encode(Player(sender_id)))
        f.close()
        await ctx.channel.send("You have registered successfully!")

@bot.command(aliases=["testdrop"])
async def drop(ctx):
    sender_id = ctx.author.id
    is_registered = os.path.exists("Players/"+str(sender_id)+".json")
    if is_registered:
        f = open("Players/"+str(sender_id)+".json", "r")
        player = jsonpickle.decode(f.read())
        f.close()
        since_last_roll = (time.time()//1)-player.last_roll_time
        player.rolls += since_last_roll//300
        if player.rolls>player.max_rolls:
            player.rolls=player.max_rolls
        if player.rolls>0:
            await generate_card_drop().sendAsMessage(ctx.channel)
            player.rolls-=1
            player.last_roll_time = time.time() - (since_last_roll % 300)
        else:
            await ctx.channel.send("You have no drops left! Next drop available in " +str(round(300-since_last_roll,1))+" seconds!")
        print(player.rolls)
        f = open("Players/"+str(sender_id)+".json", "w")
        f.write(jsonpickle.encode(player))
        f.close()
    else:
        await ctx.channel.send("You are not registered! Register with !register")


#bot.run('MTAwNjkwODA3MjQ5NDYzNzA3Ng.G3D-72.cJBtxEnMHni9K8LkgoKtHO0BkzSMBDMTJIlmZQ')
generate_card_drop().print()

if(len(sys.argv)>=2 and sys.argv[1]=='run'):
    bot.run(base64.b64decode(os.getenv('TOKEN').encode("utf-8")).decode("utf-8"))

#botthread = threading.Thread(target=bot.run, args=(base64.b64decode(os.getenv('TOKEN').encode("utf-8")).decode("utf-8") ,))
#botthread.start()
#botthread.join()