from asyncio.windows_events import NULL
import random
import idgen
from tracemalloc import start
from typing import Optional
import discord
from discord.ext import commands
import time
import os
from dotenv import load_dotenv
import base64
import sys
import Data
import databaseHandler.DataHandler
import CardArt.cardart

idGen = idgen.RandomId()
load_dotenv()
BASE_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
NOT_REGISTERED_MESSAGE = "You can't perform this action because you are not yet registered. Register with !register"
TIME_PER_ROLL = 600
TIME_PER_GRAB = 1800

cardgen = CardArt.cardart
dh = databaseHandler.DataHandler.DataHandler(".")
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
            since_last_grab = (time.time()//1)-player.last_grab_time
            player.grabs += since_last_grab//TIME_PER_GRAB
            if player.grabs>player.max_grabs:
                player.grabs=player.max_grabs
            if self.claimed:
                await interaction.response.send_message("This character has already been claimed", ephemeral=True)
            elif player.grabs>0:             
                self.claimed = True
                card_list = dh.getCards(self.character.id)
                card_id = card_list.claimCard(player.user_id)
                player.cards.append(Data.Card.Card(card_id,self.character.id))
                dh.rewriteCards(card_list, self.character.id)
                player.grabs-=1
                player.last_grab_time = time.time() - (since_last_grab % TIME_PER_GRAB)
                await interaction.response.send_message(f"{interaction.user.mention} claimed {self.character.name} Card ID: {card_id}")
            else:
                await interaction.response.send_message("You have no more grabs!", ephemeral=True)

            dh.modifyPlayer(player)
        except Exception as ex:
            print(ex)
            await interaction.response.send_message(NOT_REGISTERED_MESSAGE)
class ClaimGift(discord.ui.View):
    def __init__(self, *, timeout: float | None = 180):
        super().__init__(timeout=timeout)
        self.accepted = False
    @discord.ui.button(label="Accept",style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            player = dh.getPlayer(interaction.user.id)
            
        except Exception as ex:
            await interaction.response.send_message(NOT_REGISTERED_MESSAGE)
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

class NextPage(discord.ui.View):
    def __init__(self, book, start_page):
        super().__init__()
        self.book = book
        self.current_page = start_page-1
    @discord.ui.button(label="<-", style=discord.ButtonStyle.blurple)
    async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page > 0:
            self.current_page-=1
            embedVar = discord.Embed(title=(f"Collection"))
            embedVar.add_field(name="",value=create_page(self.book,self.current_page), inline= False)
            await interaction.response.edit_message(embed=embedVar)
    @discord.ui.button(label="->", style=discord.ButtonStyle.blurple)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page+1 < len(self.book):
            self.current_page+=1
            embedVar = discord.Embed(title=(f"Collection"))
            embedVar.add_field(name="",value=create_page(self.book,self.current_page), inline= False)
            await interaction.response.edit_message(embed=embedVar)

class BurnCard(discord.ui.View):
    def __init__(self, card_list, card_id):
        super().__init__()
        self.card_list = card_list
        self.card_id = card_id
    @discord.ui.button(label="Burn", style=discord.ButtonStyle.green)
    async def burn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("test burn")

def create_page(book, page_index):
    content = ""
    page = book[page_index]
    for card in page:
        character = characters[card.character_id]
        line = f"{card.index} **{character.name}**-{card.id} *{character.series[0]}"
        if len(line)>50:
            content+=f"{line:.47}...*\n"
        else:
            content+=f"{line:.50}*\n"
    return content

async def generate_card_drop(channel):
    random.seed(time.time())
    drop = random.choice(characters)
    mstring = f"{drop.name} from {drop.series[0]} has dropped."
    embedVar = discord.Embed(title=drop.name, description=drop.series[0], color=0x00ff00, url=drop.img_urls[0])
    embedVar.set_image(url=drop.img_urls[0])
    view1 = Claim(drop)
    await channel.send(content=mstring, embed=embedVar, view=view1)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="j",intents=intents)
@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.command(aliases=["v"])
async def view(ctx, card_index, target):
    card_index=int(card_index)
    if dh.is_registered(target):
        target = dh.getPlayer(target)
        card = target.cards[card_index]

@bot.command(aliases=["g"])
async def give(ctx, target , card_index):
    card_index=int(card_index)
    if dh.is_registered(target) and dh.is_registered(ctx.author.id):      
        giver = dh.getPlayer(ctx.author.id)
        taker = dh.getPlayer(target)
        card = giver.cards.pop(card_index)
        cards = dh.getCards(card.character_id)
        taker.cards.append(card)
        cards.cards[card.id] = taker.user_id
        dh.modifyPlayer(giver)
        dh.modifyPlayer(taker)
        dh.rewriteCards(cards, card.character_id)
        await ctx.channel.send(f"{ctx.author.mention} gave {characters[card.character_id].name} to {target}")
    else:
        await ctx.channel.send("That user is not yet registered!")

BASE_VALUE = 100
@bot.command(aliases=["b"])
async def burn(ctx, card_index):
    card_index=int(card_index)
    if dh.is_registered(ctx.author.id):
        player = dh.getPlayer(str(ctx.author.id))
        card = player.cards[card_index]
        embed = discord.Embed(title="LEMAO")
        view = BurnCard("test", 6)
        await ctx.channel.send(content="",embed=embed, view=view)


@bot.command(aliases=["$"])
async def balance(ctx, target = "user"):
    if target == "user":
        target = ctx.author.id
    if dh.is_registered(target):
        player = dh.getPlayer(str(target))
        await ctx.channel.send(f"{player.curreny}$")
@bot.command(aliases=["c"])
async def collection(ctx, target = "user", sort="index", start_page=1):
    if target == "user":
        target = ctx.author.id
    if dh.is_registered(target):
        player = dh.getPlayer(str(target))
        user = await bot.fetch_user(player.user_id)
        embedVar = discord.Embed(title=(f"{user.name}'s Collection"))
        book = player.create_book(sort, characters)
        embedVar.add_field(name="",value=create_page(book,start_page-1), inline= False)
        view1 = NextPage(book, start_page)
        await ctx.channel.send(content="",embed=embedVar, view=view1)
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

@bot.command(aliases=["cr"])
async def cardrequest(ctx):

    pass

@bot.command(aliases=["sr"])
async def seriesrequest(ctx):
    pass
@bot.command(aliases=["d"])
async def drop(ctx):
    
    pass #deprecated after this point
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
    if dh.is_registered(sender_id):
        player = dh.getPlayer(ctx.author.id)
        since_last_roll = (time.time()//1)-player.last_roll_time
        player.rolls += since_last_roll//TIME_PER_ROLL
        dropcooldown = round(TIME_PER_ROLL - (since_last_roll%TIME_PER_ROLL), 1)
        if(player.rolls)>0:
            if player.rolls >= player.max_rolls:
                player.rolls = player.max_rolls
                await ctx.channel.send(f"you have {player.rolls} drops left which is the max")
            else:
                await ctx.channel.send(f"You have no drops left, next drop is coming in {dropcooldown}")  
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
    else:
        await ctx.channel.send(NOT_REGISTERED_MESSAGE)

if(len(sys.argv)>=2 and sys.argv[1]=='run'):
    bot.run(base64.b64decode(os.getenv('TOKEN').encode("utf-8")).decode("utf-8"))