from asyncio.windows_events import NULL
import random
import idgen
from tracemalloc import start
from typing import Optional
import jsonpickle
import discord
from discord.ext import commands
import time
import os
from dotenv import load_dotenv
import base64
import sys
import DataTypes
import databaseHandler.DataHandler


dh = databaseHandler.DataHandler.DataHandler(".")

idGen = idgen.RandomId()
load_dotenv()
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
            card_list = dh.getCards(self.character.id)
            card_id = card_list.getCard()
            player.cards.append(DataTypes.Cards.Card(card_id,self.character.id))
            dh.rewriteCards(card_list, self.character.id)
            player.grabs-=1
            player.last_grab_time = time.time() - (since_last_grab % TIME_PER_GRAB)
            await interaction.response.send_message(f"{interaction.user.mention} claimed {self.character.name} Card ID: {card_id}")
        dh.modifyPlayer(player)

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
        player = dh.getPlayer(str(target))
        user = await bot.fetch_user(player.user_id)
        embedVar = discord.Embed(title=(f"{user.name}'s Collection"))
        for card in player.cards:

            embedVar.add_field(name="",value=f"**{characters[card.character_id].name}**-*{card.id}*", inline= False)
        await ctx.channel.send(content="",embed=embedVar)    

    else:
        await ctx.channel.send("That user is not yet registered!")
    
    
@bot.command(aliases=["r"])
async def register(ctx):
    sender_id = ctx.author.id

    try: 
        dh.register(sender_id)
        await ctx.channel.send("You have registered successfully!")
    except Exception as e:
        await ctx.channel.send("You are already registered!")

@bot.command(aliases=["d"])
async def drop(ctx):
    sender_id = ctx.author.id
    if(dh.is_registered(sender_id)):
        player = dh.getPlayer(sender_id)
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
        dh.modifyPlayer(player)
    else: 
        await ctx.channel.send(NOT_REGISTERED_MESSAGE)

@bot.command(aliases=["cd"])
async def cooldown(ctx):
    sender_id = ctx.author.id
    try:
        player = dh.getPlayer(sender_id)
        since_last_roll = (time.time()//1)-player.last_roll_time
        player.rolls += since_last_roll//TIME_PER_ROLL
        dropcooldown = round(TIME_PER_ROLL - (since_last_roll%TIME_PER_ROLL), 1)
        if(player.rolls)>0:
            if player.rolls >= player.max_rolls:
                player.rolls = player.max_rolls
                await ctx.channel.send(f"you have {player.rolls} drops left which is the max")
            else:
                await ctx.channel.send(f"You have {player.rolls} total drops left, next drop is coming in {dropcooldown}")  
        else:
            await ctx.channel.send(f"You have {player.rolls} drops left, next drop is coming in {dropcooldown}")
        since_last_grab = (time.time()//1)-player.last_grab_time
        player.grabs += since_last_grab//TIME_PER_GRAB
        grabcooldown = round(TIME_PER_ROLL - (since_last_grab%TIME_PER_ROLL), 1)
        if player.grabs >= player.max_grabs:
            await ctx.channel.send(f"You have {player.max_grabs} grabs left")
        elif player.grabs > 0:
            await ctx.channel.send(f"You have {player.grabs} grabs left, the next grab is coming in {grabcooldown}")
        else:
            await ctx.channel.send(f"You have no grabs loser! Take some adderall and try again in {grabcooldown} seconds")
    except:
        await ctx.channel.send(NOT_REGISTERED_MESSAGE)

if(len(sys.argv)>=2 and sys.argv[1]=='run'):
    bot.run(base64.b64decode(os.getenv('TOKEN').encode("utf-8")).decode("utf-8"))