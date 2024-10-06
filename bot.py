from asyncio.windows_events import NULL
import discord.ext
import discord.ext.commands
import idgen
from tracemalloc import start
from typing import Optional
import discord
from discord.ext import commands
import io
import os
from dotenv import load_dotenv
from sqids import Sqids
import base64
import sys
import random
import time
import Data
from Data.Card import Card as Card
from Data.Player import Player as Player
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
sqids = Sqids(alphabet="qridvCHZt3h6TeAPuEkpf8xSyQ0UcJG9lVsKj41IwaRB72MbgFmNzOoYDX5LWn", min_length=3)


class ClaimButton(discord.ui.Button["ClaimView"]):
    def __init__(self, card_index, card):
        super().__init__(style=discord.ButtonStyle.green, label=str(card_index+1))
        self.card_index=card_index
        self.card : Card = card

    async def callback(self, interaction: discord.Interaction):
        if not(player := await get_player(interaction, interaction.user.id)):
            return
        player : Player
        since_last_grab = time.time()-player.last_grab_time
        if since_last_grab < TIME_PER_GRAB:
            await interaction.response.send_message(f"{interaction.user.mention} you have no more grabs! Your next grab is available in {(TIME_PER_GRAB-since_last_grab):.1f} seconds!",ephemeral=True)
            return
        player.last_grab_time = time.time()
        self.disabled = True
        self.set_claim(player)
        sqid_id = sqids.encode([self.card.card_id])
        await interaction.response.send_message(f"{interaction.user.mention} claimed the {self.card.character.name} card! (ID: `{sqid_id}`)")

    def set_claim(self, player : Player):
        self.card.claim_id()
        self.card.set_owner(player)
        player.claim(self.card)
        dh.save_player(player)
        dh.save_card(self.card)
        
class ClaimView(discord.ui.View):
    def __init__(self, cards):
        super().__init__()
        self.cards=cards
        for i in range(0,len(cards)):
            self.add_item(ClaimButton(i, cards[i]))

class CardView(discord.ui.View):
    def __init__(self, card):
        super().__init__()
        self.card : Card = card
    @discord.ui.button(label="Stats", style=discord.ButtonStyle.green)
    async def stats(self, interaction: discord.Interaction, button: discord.Button):
        embed = discord.Embed(title=(f"{self.card.character.name}"))
        embed.add_field(name="",value=self.card.get_embed())
        await interaction.response.edit_message(embed=embed)

async def generate_drop(ctx):
    seed = time.time()
    random.seed(seed)
    cards = []
    image = Image.new("RGBA",(1300,600))
    for i in range(3):
        card = Data.Card.Card(random.choice(list(characters.values())), seed+i)
        cards.append(card)
        image.paste(card.image(), (450*i,0))
    view1 = ClaimView(cards)
    await ctx.channel.send(f"{ctx.author.mention} is dropping cards",file=create_file(image), view=view1)


def create_file(image):
    with io.BytesIO() as buffer:
        image.save(buffer, format="PNG")
        buffer.seek(0)
        file = discord.File(fp=buffer,filename="test.png")
    return file

async def get_player(ctx, id=None):
    id = ctx.author.id if id is None else id
    if dh.is_registered(id):
        player : Player = dh.get_player(id)
        return player
    else:
        await ctx.channel.send(NOT_REGISTERED)
        return False
    

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")


@bot.command(aliases=[])
async def register(ctx):
    print(ctx)
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
    if not(player := await get_player(ctx)):
        return
    since_last_drop = (time.time()//1)-player.last_drop_time
    player.drops += since_last_drop//TIME_PER_DROP
    if player.drops<=0:
        await ctx.channel.send(f"You have no drops left! Next drop available in {(TIME_PER_DROP-since_last_drop):.1f} seconds!")
        dh.save_player(player)
        return
    if player.drops >= MAX_DROPS:
        player.drops = MAX_DROPS
    player.drops-=1
    await generate_drop(ctx)
    player.last_drop_time = time.time() - (since_last_drop % TIME_PER_DROP)
    dh.save_player(player)


@bot.command(aliases=["c","card"])
async def view_card(ctx, sqid_card_id=None):
    if not(player := await get_player(ctx)):
        return
    if sqid_card_id:
        card_id = sqids.decode(sqid_card_id)[0]
    else:
        card_id = player.inventory.cards
    if card := dh.get_card(card_id):
        image = card.image()
        await ctx.channel.send(f"{card.character.name}",file=create_file(image), view=CardView(card))
    else:
        await ctx.channel.send(f"Card not found!")


bot.run(os.getenv('TOKEN')) 