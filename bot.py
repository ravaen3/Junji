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
<<<<<<< Updated upstream
import data
=======
import DataTypes
import databaseHandler


dh = databaseHandler.DataHandler(".")
>>>>>>> Stashed changes

idGen = idgen.RandomId()
load_dotenv()
sqids = Sqids(alphabet="kEjqW4T673ePsJNoACFwUVy1Ofabmz5nxGDtcHZQ2lpgrSLdhM0uR8iKIvBX9Y", min_length=4)
BASE_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
NOT_REGISTERED_MESSAGE = "You can't perform this action because you are not yet registered. Register with !register"
TIME_PER_ROLL = 300
TIME_PER_GRAB = 1200

characters = dh.getCharacters()
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
                f = open("Cards/data.json", "r+")
                cards = jsonpickle.decode(f.read())
                for i in range(1,10000):
                    card_id = idGen.getFullString(self.character.id, i)
                    if card_id not in cards:
                        cards[card_id] = CardListing(card_id, interaction.user.id)
                        await interaction.response.send_message(interaction.user.mention+ " claimed " + self.character.name + "Card ID: " + card_id)
                        break
                f.seek(0)
                f.write(jsonpickle.encode(cards))
                f.close()
                player.cards.append(Card(card_id,self.character))
                player.grabs-=1
                player.last_grab_time = time.time() - (since_last_grab % TIME_PER_GRAB)
            else:
                await interaction.response.send_message("You have no grabs left! Next grab available in " +str(round(TIME_PER_GRAB-since_last_grab,1))+" seconds!", ephemeral=True)
            f = open("Players/"+str(interaction.user.id)+".json", "w")
            f.write(jsonpickle.encode(player))
            f.close()
        else:
            await interaction.response.send_message(NOT_REGISTERED_MESSAGE)
<<<<<<< Updated upstream
=======
            return
        since_last_grab = (time.time()//1)-player.last_grab_time
        player.grabs += since_last_grab//TIME_PER_GRAB
        if player.grabs>player.max_grabs:
            player.grabs=player.max_grabs
        if self.claimed:
            await interaction.response.send_message("This character has already been claimed", ephemeral=True)
        elif player.grabs>0:             
            self.claimed = True
            card_list = dh.getCards(self.character.id)
            card_id = card_list.getCard()
            player.cards.append(DataTypes.Cards.Card(card_id,self.character.id))
            dh.rewriteCards(card_list, self.character.id)
            #player.cards.append(DataTypes.Cards.Card(card_id,self.character.id))
            player.grabs-=1
            player.last_grab_time = time.time() - (since_last_grab % TIME_PER_GRAB)
            await interaction.response.send_message(f"{interaction.user.mention} claimed {self.character.name} Card ID: {card_id}")
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
>>>>>>> Stashed changes

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

def load_data():
    f = open("data.json")
    botdata = jsonpickle.decode(f.read())
    f.close()
def load_characters():
    f = open("Characters/data.json", "r")
    data = jsonpickle.decode(f.read())
    f.close()
    return data

async def generate_card_drop(channel):
    random.seed(time.time())
    drop = random.choice(characters)
    mstring = f"{drop.name} from {drop.series[0]} has dropped."
    embedVar = discord.Embed(title=drop.name, description=drop.series[0], color=0x00ff00, url=drop.img_urls[0])
    embedVar.set_image(url=drop.img_urls[0])
    view1 = Claim(drop)
    await channel.send(content=mstring, embed=embedVar, view=view1)
def load_card():
    pass
<<<<<<< Updated upstream
characters = load_characters()
=======
>>>>>>> Stashed changes

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!",intents=intents)
@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
@bot.command(aliases=["c"])
async def collection(ctx, target = "user"):
    if target == "user":
        target = ctx.author.id
    else:
        print(target)
    is_registered = os.path.exists("Players/"+str(target)+".json")
    if is_registered:
<<<<<<< Updated upstream
        f = open("Players/"+str(target)+".json")
        player = jsonpickle.decode(f.read())
        f.close()
        await player.collection(ctx.channel)
=======
        player = dh.getPlayer(str(target))
        user = await bot.fetch_user(player.user_id)
        embedVar = discord.Embed(title=(f"{user.name}'s Collection"))
        for card in player.cards:

            embedVar.add_field(name="",value=f"**{characters[card.character_id].name}**-*{card.id}*", inline= False)
        await ctx.channel.send(content="",embed=embedVar)    
>>>>>>> Stashed changes

    else:
        await ctx.channel.send("That user is not yet registered!")
    
    
@bot.command(aliases=["r"])
async def register(ctx):
    sender_id = ctx.author.id
    is_registered = os.path.exists("Players/"+str(sender_id)+".json")
    if is_registered:
        await ctx.channel.send("You are already registered!")
<<<<<<< Updated upstream
    else:
        f = open("Players/"+str(sender_id)+".json", "w")
        f.write(jsonpickle.encode(Player(sender_id)))
        f.close()
        await ctx.channel.send("You have registered successfully!")
=======
>>>>>>> Stashed changes

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
            await generate_card_drop(ctx.channel)
            player.rolls-=1
            player.last_roll_time = time.time() - (since_last_roll % TIME_PER_ROLL)
        else:
            await ctx.channel.send("You have no drops left! Next drop available in " +str(round(TIME_PER_ROLL-since_last_roll,1))+" seconds!")
<<<<<<< Updated upstream
        print(player.rolls)
        f = open("Players/"+str(sender_id)+".json", "w")
        f.write(jsonpickle.encode(player))
        f.close()
    else:
        await ctx.channel.send(NOT_REGISTERED_MESSAGE)


#bot.run('MTAwNjkwODA3MjQ5NDYzNzA3Ng.G3D-72.cJBtxEnMHni9K8LkgoKtHO0BkzSMBDMTJIlmZQ')

=======
        dh.modifyPlayer(player)
    else: 
        await ctx.channel.send(NOT_REGISTERED_MESSAGE)

>>>>>>> Stashed changes
if(len(sys.argv)>=2 and sys.argv[1]=='run'):
    bot.run(base64.b64decode(os.getenv('TOKEN').encode("utf-8")).decode("utf-8"))

#botthread = threading.Thread(target=bot.run, args=(base64.b64decode(os.getenv('TOKEN').encode("utf-8")).decode("utf-8") ,))
#botthread.start()
#botthread.join()