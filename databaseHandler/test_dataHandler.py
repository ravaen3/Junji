import DataHandler




dh = DataHandler.DataHandler(".")

dh.register(0)
for i in range(0, 3):
    
    dh.getCharacter(i)
    print(dh.getPlayer(i))
    