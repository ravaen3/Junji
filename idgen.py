
class RandomId:
    def getFullString(self, charid, cardid):
        return self.__getCharString(self.__getCharId(charid)) + "-" + self.__getCharString(self.__getCharId(cardid + (charid+1)))

    def getCardString(self, charid, cardid):
        return self.__getCharString(self.__getCharId(charid + cardid))
    
    def getCharString(self, charid):
        return self.__getCharString(self.__getCharId(charid))


    def stringReverse(self, charstring):
        return self.__reverseCharId(self.__reverseCharString(charstring))

    def __getCharId(self, id):
        alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789?!"
        aux = 0
        maxbits = 128
        size = 18 #size is the floor( 2log( len(alphabet) ** len(code) ) ) 
        idcopy = id
        for i in range(0,size):
            aux *=2
            aux = aux + ( 1 if self.__getBitNumber(13*(i) % size) & idcopy > 0 else 0)
        for i in range(size,maxbits):
            aux += self.__getBitNumber(i) & idcopy
        return aux

    def __reverseCharId(self, id):
        size = 18 #size is the floor( 2log( len(alphabet) ** len(code) ) ) 
        aux = 0
        idcopy = id
        maxbits = 128
        for i in range(0, size):
            if(idcopy & 1 > 0):
                aux = aux + self.__getBitNumber(13*(size-i-1) % size)
            idcopy = idcopy >> 1
        for j in range(size, maxbits):
            aux += id & (self.__getBitNumber(j))
        return aux


    def __getCharString(self, id):
        alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789?!"
        idcopy = id
        if id ==0:
            return "a"
        res = ""

        #for i in range(0,3):
            #res += alphabet[idcopy % 62]
            #idcopy = idcopy//62
        
        while(idcopy>0):
            res += alphabet[idcopy % 64]
            idcopy = idcopy//64
        return res

    def __reverseCharString(self, s):
        alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789?!"
        res = 0
        for i in range(len(s)):
            res += alphabet.find(s[i]) * 64**i
        return res

    def __getBitNumber(self, id):
        if(id<0):
            print("can not get this bitnumber")
            exit(1)
        aux = 1
        while(id>0):
            aux = aux << 1
            id -= 1
        return aux

    def __base62(int, alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"):
        if int<62:
            return alphabet[int]
        else:
            return self.__base62(int//62, alphabet) + alphabet[int % 62]



