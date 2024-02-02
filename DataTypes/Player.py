import discord
import databaseHandler
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
    async def collection(self, channel, bot):
        print(self.user_id)
        user = await bot.fetch_user(self.user_id)
        embedVar = discord.Embed(title=(f"{user.name}'s Collection"))
        for card in self.cards:
            embedVar.add_field(name=card.id, value=card.character.name)
        await channel.send(content="test",embed=embedVar)