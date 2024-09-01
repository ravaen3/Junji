from asyncio.windows_events import NULL
import idgen
from tracemalloc import start
from typing import Optional
import discord
from discord.ext import commands
import io
import os
from dotenv import load_dotenv
import base64
import sys
import random
import time
import Data
import Data.Card
import Data.DataHandler
from PIL import Image
dh = Data.DataHandler.DataHandler("Data")
cIDg = Data.DataHandler.IDGen()

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
prefix = "j"
bot = commands.Bot(command_prefix=prefix,intents=intents)
characters = dh.get_characters()
NOT_REGISTERED=f"You are not registered, register with `{prefix}register`"


class Claim(discord.ui.View):
    def __init__(self,character):
        super().__init__()
        self.characters=characters
    @discord.ui.button(label="1", style=discord.ButtonStyle.green)
    async def claim1(self, interaction: discord.Interaction, button: discord.ui.Button):
        player = dh.is_registered(interaction.user.id)
        if player:
            pass

async def generate_drop(ctx):
    seed = time.time()
    random.seed(seed)
    cards = []
    image = Image.new("RGBA",(1300,600))
    for i in range(3):
        card = Data.Card.Card(random.choice(list(characters.values())), seed+i)
        cards.append(card)
        image.paste(card.image(), (450*i,0))
        
    with io.BytesIO() as buffer:
        image.save(buffer, format="PNG")
        file = discord.File(fp=buffer,filename="test.png")
        buffer.seek(0)
        await ctx.channel.send(file=file)

async def get_player(ctx, id=None):
    id = ctx.author.id if id is None else id
    if dh.is_registered(id):
        return dh.get_player(id)
    else:
        await ctx.channel.send(NOT_REGISTERED)
        return False
@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.command(aliases=[])
async def register(ctx):
    sender_id= ctx.author.id
    if dh.is_registered(sender_id):
        await ctx.channel.send("You are already registered!")
    else:
        dh.register(sender_id)
        await ctx.channel.send("You are now registered!")
TIME_PER_DROP = 30
MAX_DROPS = 3
@bot.command(aliases=["d"])
async def drop(ctx):
    player = await get_player(ctx)
    if player:
        since_last_drop = (time.time()//1)-player.last_drop_time
        player.drops += since_last_drop//TIME_PER_DROP
        if player.drops>0:
            if player.drops >= MAX_DROPS:
                player.drops = MAX_DROPS
            player.drops-=1
            await generate_drop(ctx)
            player.last_drop_time = time.time() - (since_last_drop % TIME_PER_DROP)
        else:
            await ctx.channel.send(f"You have no drops left! Next drop available in {str(round(TIME_PER_DROP-since_last_drop,1))} seconds!")
        player.save()





#if(len(sys.argv)>=2 and sys.argv[1]=='run'):
bot.run(base64.b64decode(os.getenv('TOKEN').encode("utf-8")).decode("utf-8"))