from os import name
from pyparsing import Char
import re
import requests
import time
import jsonpickle
import random
from sqids import Sqids
from bs4 import BeautifulSoup
class Character:
    def __init__(self, name, series, art_urls = {}):
        #short
        self.name = name
        self.series = series
        self.art_urls = art_urls
        #game stats
        self.wishlists = 0
characters = {}
URL = "https://leagueoflegends.fandom.com/wiki/List_of_champions"
html = BeautifulSoup(requests.get(URL).text)
for entry in html.find_all("span", attrs={"style":"white-space:normal;"}):
    if entry.find("a"):
        if not entry.find("a").has_attr("class"):
            character_name= entry.find("a")["title"]
            if character_name.endswith("/LoL"):
                characters[f"{character_name[:-4]} League_of_Legends"]=(Character(character_name[:-4],"League of Legends",{"0":"https://cdn.discordapp.com/attachments/464939388061745163/1220845872041033758/image.png?ex=66106c52&is=65fdf752&hm=841f31f48a0838484d7d808b58838474defa1d1472d10aab17ae945caab39cc0&"}))
f = open("league.json","w")
f.write(jsonpickle.encode(characters))
f.close()
