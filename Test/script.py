import jsonpickle

class Mutable():
    def __init__(self, minun):
        self.minun = minun
        self.minun2 = "<<33"
    def update(self):
        clone = Mutable("<3")
        for attr in dir(clone):
            if hasattr(self, attr):
                pass
            else:
                self.__setattr__(attr,getattr(clone, attr))




f = open("minun.json", "r")
test = jsonpickle.decode(f.read())
f.close()
test.update()
print(test.minun2)