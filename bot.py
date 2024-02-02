from asyncio.windows_events import NULL
import asyncio
import random
import idgen
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
import data
import DataTypes
import databaseHandler


dh = databaseHandler.DataHandler.DataHandler(".")

idGen = idgen.RandomId()
load_dotenv()
sqids = Sqids(alphabet="kEjqW4T673ePsJNoACFwUVy1Ofabmz5nxGDtcHZQ2lpgrSLdhM0uR8iKIvBX9Y", min_length=4)
BASE_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
NOT_REGISTERED_MESSAGE = "You can't perform this action because you are not yet registered. Register with !register"
TIME_PER_ROLL = 300
TIME_PER_GRAB = 1200

class BotData(object):
    pass
class Claim(discord.ui.View):
    def __init__(self, character):
        super().__init__()
        self.value = None
        self.claimed = False
        self.character = character
    @discord.ui.button(label='Claim', style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            player = dh.getPlayer(interaction.user.id)
        except Exception as ex:
            await interaction.response.send_message(NOT_REGISTERED_MESSAGE)
            return
        since_last_grab = (time.time()//1)-player.last_grab_time
        player.grabs += since_last_grab//TIME_PER_GRAB
        if player.grabs>player.max_grabs:
            player.grabs=player.max_grabs
        if self.claimed:
            await interaction.response.send_message("This character has already been claimed", ephemeral=True)
        elif player.grabs>0:             
            self.claimed = True
            cards = dh.getCards()

            for i in range(1,10000):
                card_id = idGen.getFullString(self.character.id, i)
                if card_id not in cards:
                    cards[card_id] = DataTypes.CardListing(card_id, interaction.user.id)
                    await interaction.response.send_message(interaction.user.mention+ " claimed " + self.character.name + "Card ID: " + card_id)
                    break

            dh.rewriteCards(cards)
            player.cards.append(DataTypes.Card(card_id,self.character))
            player.grabs-=1
            player.last_grab_time = time.time() - (since_last_grab % TIME_PER_GRAB)
        dh.modifyPlayer(player)
       
        # ############
        # is_registered = os.path.exists("Players/"+str(interaction.user.id)+".json")
        
        # if is_registered:
        #     f = open("Players/"+str(interaction.user.id)+".json", "r")
        #     player = jsonpickle.decode(f.read())
        #     f.close()
        #     since_last_grab = (time.time()//1)-player.last_grab_time
        #     player.grabs += since_last_grab//TIME_PER_GRAB
        #     if player.grabs>player.max_grabs:
        #         player.grabs=player.max_grabs
        #     if self.claimed:
        #         await interaction.response.send_message("This character has already been claimed", ephemeral=True)
        #     elif player.grabs>0:             
        #         self.claimed = True
        #         f = open("Cards/data.json", "r+")
        #         cards = jsonpickle.decode(f.read())
        #         for i in range(1,10000):
        #             card_id = idGen.getFullString(self.character.id, i)
        #             if card_id not in cards:
        #                 cards[card_id] = CardListing(card_id, interaction.user.id)
        #                 await interaction.response.send_message(interaction.user.mention+ " claimed " + self.character.name + "Card ID: " + card_id)
        #                 break
        #         f.seek(0)
        #         f.write(jsonpickle.encode(cards))
        #         f.close()
        #         player.cards.append(Card(card_id,self.character))
        #         player.grabs-=1
        #         player.last_grab_time = time.time() - (since_last_grab % TIME_PER_GRAB)
        #     else:
        #         await interaction.response.send_message("You have no grabs left! Next grab available in " +str(round(TIME_PER_GRAB-since_last_grab,1))+" seconds!", ephemeral=True)
            
        #     f = open("Players/"+str(interaction.user.id)+".json", "w")
        #     f.write(jsonpickle.encode(player))
        #     f.close()
        #     ########
        # else:
        #     await interaction.response.send_message(NOT_REGISTERED_MESSAGE)

class Character:
    def __init__(self, name, id, series, img_urls ="test"):
        self.name = name
        self.id = id
        self.series = series
        self.img_urls = img_urls
    def print(self):
        print(f"name={self.name}")
        print(f"series={self.series[0]}")
        print(f"img_urls={self.img_urls[0]}")
    async def sendAsDrop(self, channel):
        self.print()
        name = self.name.replace("_"," ")
        mstring = f"{name} from {self.series[0]} has dropped."
        embedVar = discord.Embed(title=self.name, description=self.series[0], color=0x00ff00, url=self.img_urls[0])
        embedVar.set_image(url=self.img_urls[0])
        view1 = Claim(self)
        await channel.send(content=mstring, embed=embedVar, view=view1)

class CardListing:
    def __init__(self, id, owner_id):
        self.id = id
        self.owner_id = owner_id
class CardOptions:
    def __init__(self):
        self.img = 0
class Card:
    def __init__(self, id, character):
        self.id = id
        self.character = character
        self.options = CardOptions()
    async def sendAsCard(self, channel):
        name = self.character.name.replace("_"," ")

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
    async def collection(self, channel):
        print(self.user_id)
        user = await bot.fetch_user(self.user_id)
        embedVar = discord.Embed(title=(f"{user.name}'s Collection"))
        for card in self.cards:
            embedVar.add_field(name=card.id, value=card.character.name)
        await channel.send(content="test",embed=embedVar)

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
# characters = load_characters()
characters = dh.getCharacters()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!",intents=intents)
@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    print(bot.user.id)
@bot.command(aliases=["c"])
async def collection(ctx, target = "user"):
    if target == "user":
        target = ctx.author.id
    else:
        print(target)
    is_registered = os.path.exists("Players/"+str(target)+".json")
    if is_registered:
        player = dh.getPlayer(str(target))
        # f = open("Players/"+str(target)+".json")
        # player = jsonpickle.decode(f.read())
        # f.close()
        await player.collection(ctx.channel)

    else:
        await ctx.channel.send("That user is not yet registered!")
    
    
@bot.command(aliases=["r"])
async def register(ctx):
    sender_id = ctx.author.id

    try: 
        dh.register(sender_id)
        await ctx.channel.send("You have registered successfully!")
    except:
        await ctx.channel.send("You are already registered!")
    
    # is_registered = os.path.exists("Players/"+str(sender_id)+".json")
    # if is_registered:
    #     await ctx.channel.send("You are already registered!")
    # else:
    #     f = open("Players/"+str(sender_id)+".json", "w")
    #     f.write(jsonpickle.encode(Player.Player(sender_id)))
    #     f.close()
    #     await ctx.channel.send("You have registered successfully!")

@bot.command(aliases=["testdrop"])
async def drop(ctx):
    sender_id = ctx.author.id
    if(dh.is_registered(sender_id)):
        player = dh.getPlayer(sender_id)
        since_last_roll = (time.time()//1)-player.last_roll_time
        player.rolls += since_last_roll//TIME_PER_ROLL
        if player.rolls>player.max_rolls:
            player.rolls=player.max_rolls
        if player.rolls>0:
            await generate_card_drop().sendAsDrop(ctx.channel)
            player.rolls-=1
            player.last_roll_time = time.time() - (since_last_roll % TIME_PER_ROLL)
        else:
            await ctx.channel.send("You have no drops left! Next drop available in " +str(round(TIME_PER_ROLL-since_last_roll,1))+" seconds!")
        print(player.rolls)
        dh.modifyPlayer(player)
    else: 
        await ctx.channel.send(NOT_REGISTERED_MESSAGE)


    # is_registered = os.path.exists("Players/"+str(sender_id)+".json")
    # if is_registered:
    #     f = open("Players/"+str(sender_id)+".json", "r")
    #     player = jsonpickle.decode(f.read())
    #     f.close()
    #     since_last_roll = (time.time()//1)-player.last_roll_time
    #     player.rolls += since_last_roll//TIME_PER_ROLL
    #     if player.rolls>player.max_rolls:
    #         player.rolls=player.max_rolls
    #     if player.rolls>0:
    #         await generate_card_drop().sendAsDrop(ctx.channel)
    #         player.rolls-=1
    #         player.last_roll_time = time.time() - (since_last_roll % TIME_PER_ROLL)
    #     else:
    #         await ctx.channel.send("You have no drops left! Next drop available in " +str(round(TIME_PER_ROLL-since_last_roll,1))+" seconds!")
    #     print(player.rolls)
    #     f = open("Players/"+str(sender_id)+".json", "w")
    #     f.write(jsonpickle.encode(player))
    #     f.close()
    # else:
    #     await ctx.channel.send(NOT_REGISTERED_MESSAGE)


#bot.run('MTAwNjkwODA3MjQ5NDYzNzA3Ng.G3D-72.cJBtxEnMHni9K8LkgoKtHO0BkzSMBDMTJIlmZQ')

if(len(sys.argv)>=2 and sys.argv[1]=='run'):
    bot.run(base64.b64decode(os.getenv('TOKEN').encode("utf-8")).decode("utf-8"))

#botthread = threading.Thread(target=bot.run, args=(base64.b64decode(os.getenv('TOKEN').encode("utf-8")).decode("utf-8") ,))
#botthread.start()
#botthread.join()