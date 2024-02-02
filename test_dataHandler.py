import databaseHandler
import DataTypes



dh = databaseHandler.DataHandler(".")

cl = DataTypes.CardListing(000, 000)
print(cl)
dh.addCard(cl)
exit(0)
for i in range(0, 5):
  
    dh.getCharacter(i)
    print(dh.getPlayer(i))
    