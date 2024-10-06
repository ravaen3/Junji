import Data.DataHandler
dh = Data.DataHandler.DataHandler("Data")
import jsonpickle
import os
characters = dh.get_characters()

series_count = {}
print(characters)
for character in characters:
    for anime in characters[character].series:  
        if anime in series_count:
            series_count[anime]+=1
        else:
            series_count[anime]=1
series_list = sorted(series_count, key= series_count.get, reverse=True)

for character in characters:
    character.series=[x for x in series_list if x in frozenset(characters[character].series)]
    character.series=[ characters[character].series[0]]
f = open("Data\Characters\data.json", "w")
f.write(jsonpickle.encode(characters))
f.close()

