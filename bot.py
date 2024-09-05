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
TIME_PER_GRAB = 30
class ClaimButton(discord.ui.Button["ClaimView"]):
    def __init__(self, card_index, card):
        super().__init__(style=discord.ButtonStyle.green, label=str(card_index+1))
        self.card_index=card_index
        self.card=card
    async def callback(self, interaction: discord.Interaction):
        player = await get_player(interaction, interaction.user.id)
        if not player:
            return
        since_last_grab = time.time()-player.last_grab_time
        if since_last_grab < TIME_PER_GRAB:
            await interaction.response.send_message(f"{interaction.user.mention} you have no more grabs! Your next grab is available in {(TIME_PER_GRAB-since_last_grab):.1f} seconds!",ephemeral=True)
            return
        player.last_grab_time = time.time()
        self.disabled = True
        player.inventory.cards.append(self.card)
        player.save()
        await interaction.response.send_message(f"{interaction.user.mention} claimed the {self.card.character.name} card!")
    pass
class ClaimView(discord.ui.View):
    def __init__(self,cards):
        super().__init__()
        self.cards=cards
        for i in range(0,len(cards)):
            self.add_item(ClaimButton(i, cards[i]))

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
        view1 = ClaimView(cards)
        await ctx.channel.send(file=file, view=view1)

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
    if not player:
        return
    since_last_drop = (time.time()//1)-player.last_drop_time
    player.drops += since_last_drop//TIME_PER_DROP
    if player.drops<=0:
        await ctx.channel.send(f"You have no drops left! Next drop available in {(TIME_PER_DROP-since_last_drop):.1f} seconds!")
        player.save()
        return
    if player.drops >= MAX_DROPS:
        player.drops = MAX_DROPS
    player.drops-=1
    await generate_drop(ctx)
    player.last_drop_time = time.time() - (since_last_drop % TIME_PER_DROP)
    player.save()





#if(len(sys.argv)>=2 and sys.argv[1]=='run'):
bot.run(os.getenv('TOKEN'))