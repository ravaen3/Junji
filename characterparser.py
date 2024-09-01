import databaseHandler.DataHandler
dh = databaseHandler.DataHandler.DataHandler(".")
import jsonpickle
import os
characters = dh.getCharacters()

series_count = {}

for character in characters:
    for anime in character.series:
        if anime in series_count:
            series_count[anime]+=1
        else:
            series_count[anime]=1
series_list = sorted(series_count, key= series_count.get, reverse=True)

for character in characters:
    character.series=[x for x in series_list if x in frozenset(character.series)]
f = open("Characters\data.json", "w")
f.write(jsonpickle.encode(characters))
f.close()

