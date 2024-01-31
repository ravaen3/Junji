from os import name
from pyparsing import Char
import re
import requests
import time
import jsonpickle
import random
from sqids import Sqids
from bs4 import BeautifulSoup
character_amount = 5000
series_whitelist = [] #"https://myanimelist.net/anime/8234/Muumin"
series_names = ["One Piece", "Dragon Ball", "Shingeki no Kyojin", "Sousou no Frieren"]
amount_scraped = 0
class Character:
    def __init__(self, name, series, img_url ="test"):
        self.name = name
        self.series = series
        self.img_urls = [img_url]

characters = {}
for i in range(0,character_amount//50):
    URL = ("https://myanimelist.net/character.php?limit="+str(i*50))
    html = BeautifulSoup(requests.get(URL).text)
    if len(html.find_all("tr", attrs={"class":"ranking-list"}))<10:
        time.sleep(random.randint(10,20))
        print("Failure to load site, trying again...")
        html = BeautifulSoup(requests.get(URL).text)
    for entry in html.find_all("tr", attrs={"class":"ranking-list"}):
        name = re.findall("(?<=\d\/)(.*?)(?=\")",str(entry.find("a", attrs={"class":"fs14 fw-b"})))[0]
        series = ""
        series_arr = entry.find("td", attrs={"class":"animeography"}).find_all("a")
        series_arr.extend(entry.find("td", attrs={"class":"mangaography"}).find_all("a"))
        for anime in series_arr:
            if anime.get_text() in series_names:
                series = anime.get_text()
                break
            if len(anime.get_text())<len(series) or series == "":
                series = anime.get_text() 
        image_id = re.findall("(?<=rs\/)(.*?)\?", str(entry.find("img", attrs={"class":"lazyload"})))
        image_url = "https://upload.wikimedia.org/wikipedia/commons/8/89/Portrait_Placeholder.png"
        if len(image_id) != 0:
            image_url = "https://cdn.myanimelist.net/images/characters/" +image_id[0]
       
        character = Character(
            re.findall("(?<=\d\/)(.*?)(?=\")",str(entry.find("a", attrs={"class":"fs14 fw-b"})))[0],
            str(series),
            image_url
        )
        characters[name]=character
        print(amount_scraped)
        amount_scraped+=1
    time.sleep(random.randint(8,12))
for URL in series_whitelist:
    html = BeautifulSoup(requests.get(URL+"/characters").text)
    for entry in html.find("div", attrs={"class":"rightside js-scrollfix-bottom-rel"}).find_all("table", attrs={"class":"js-anime-character-table"}):
        print(entry.find("h3"))
f = open("Characters/data.json", "w")
f.write(jsonpickle.encode(characters))
f.close()