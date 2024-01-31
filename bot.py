from asyncio.windows_events import NULL
import asyncio
import random
from tracemalloc import start
from typing import Optional
import jsonpickle
import discord
from discord.ext import commands
import time
import os
from sqids import Sqids
from dotenv import load_dotenv
import base64
import sys

load_dotenv()
sqids = Sqids(alphabet="kEjqW4T673ePsJNoACFwUVy1Ofabmz5nxGDtcHZQ2lpgrSLdhM0uR8iKIvBX9Y", min_length=4)
BASE_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
NOT_REGISTERED_MESSAGE = "You can't perform this action because you are not yet registered. Register with !register"
TIME_PER_ROLL = 300
TIME_PER_GRAB = 1800

class BotData(object):
    pass
class Claim(discord.ui.View):
    def __init__(self, name):
        super().__init__()
        self.value = None
        self.claimed = False
        self.character_name = name
    @discord.ui.button(label='Claim', style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        is_registered = os.path.exists("Players/"+str(interaction.user.id)+".json")
        if is_registered:
            f = open("Players/"+str(interaction.user.id)+".json", "r")
            player = jsonpickle.decode(f.read())
            f.close()
            since_last_grab = (time.time()//1)-player.last_grab_time
            player.grabs += since_last_grab//TIME_PER_GRAB
            if player.grabs>player.max_grabs:
                player.grabs=player.max_grabs
            if self.claimed:
                await interaction.response.send_message("This character has already been claimed", ephemeral=True)
            elif player.grabs>0:
                self.claimed = True
                await interaction.response.send_message(interaction.user.mention+ " claimed " + self.character_name)
                player.grabs-=1
                player.last_grab_time = time.time() - (since_last_grab % TIME_PER_GRAB)
            else:
                await interaction.response.send_message("You have no grabs left! Next grab available in " +str(round(TIME_PER_GRAB-since_last_grab,1))+" seconds!", ephemeral=True)
            f = open("Players/"+str(interaction.user.id)+".json", "w")
            f.write(jsonpickle.encode(player))
            f.close()
        else:
            await interaction.response.send_message(NOT_REGISTERED_MESSAGE)

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
        view1 = Claim(name)
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
        self.max_grabs = 2
        self.last_roll_time = 0
        self.last_grab_time = 0
        self.cards = []
        self.upgrades = []
        self.inventory = []

def base62(x, alphabet = BASE_ALPHABET, i=0, min_length = 3):
    if x < 62 and i == min_length-1:
        return alphabet[x%62]
    else:
        return base62(x // 62, alphabet, i+1) + alphabet[x % 62]

def base10(x, alphabet = BASE_ALPHABET):
    base = len(alphabet)
    y = 0
    for char in x:
        y = y * base + alphabet.index(char)
    return y

def shuffle(string, seed = 1):
    random.seed(seed)
    chars = list(string)
    random.shuffle(chars)
    return "".join(chars)

def generate_card_hexid(character_id,card_id):
    character_hexid = base62(character_id)
    card_hexid = character_hexid+str(base62(card_id,shuffle(BASE_ALPHABET, character_id)))
    return card_hexid
def load_data():
    f = open("data.json")
    botdata = jsonpickle.decode(f.read())
    f.close()
def load_characters():
    f = open("Characters/data.json", "r")
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
        player.rolls += since_last_roll//TIME_PER_ROLL
        if player.rolls>player.max_rolls:
            player.rolls=player.max_rolls
        if player.rolls>0:
            await generate_card_drop().sendAsMessage(ctx.channel)
            player.rolls-=1
            player.last_roll_time = time.time() - (since_last_roll % TIME_PER_ROLL)
        else:
            await ctx.channel.send("You have no drops left! Next drop available in " +str(round(TIME_PER_ROLL-since_last_roll,1))+" seconds!")
        print(player.rolls)
        f = open("Players/"+str(sender_id)+".json", "w")
        f.write(jsonpickle.encode(player))
        f.close()
    else:
        await ctx.channel.send(NOT_REGISTERED_MESSAGE)


#bot.run('MTAwNjkwODA3MjQ5NDYzNzA3Ng.G3D-72.cJBtxEnMHni9K8LkgoKtHO0BkzSMBDMTJIlmZQ')
generate_card_drop().print()

if(len(sys.argv)>=2 and sys.argv[1]=='run'):
    bot.run(base64.b64decode(os.getenv('TOKEN').encode("utf-8")).decode("utf-8"))

#botthread = threading.Thread(target=bot.run, args=(base64.b64decode(os.getenv('TOKEN').encode("utf-8")).decode("utf-8") ,))
#botthread.start()
#botthread.join()