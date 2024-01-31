



def getCharId(id):
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    aux = 0
    maxbits = 32
    size = 18 #size is the floor( 2log( len(alphabet) ** len(code) ) ) 
    idcopy = id
    for i in range(0,size):
        aux *=2
        aux = aux + ( 1 if getBitNumber(13*i % size) & idcopy > 0 else 0)
    for i in range(size,maxbits):
        aux += getBitNumber(i) & idcopy
    return aux

def reverseCharId(id):
    size = 18 #size is the floor( 2log( len(alphabet) ** len(code) ) ) 
    aux = 0
    idcopy = id
    maxbits = 32
    for i in range(0, size):
        if(idcopy & 1 > 0):
            aux = aux + getBitNumber(13*(size-i-1) % size)
        idcopy = idcopy >> 1
    for j in range(size, maxbits):
        aux += id & (getBitNumber(j))
    return aux


def getCharString(id):
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    idcopy = id
    res = ""
    for i in range(0,3):
        res += alphabet[idcopy % 62]
        idcopy = idcopy//62
    
    while(idcopy>0):
        res += alphabet[idcopy % 62]
        idcopy = idcopy//62
    return res

def reverseCharString(s):
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    res = 0
    for i in range(len(s)):
        res += alphabet.find(s[i]) * 62**i
    return res
    return alphabet.find(s[0]) + alphabet.find(s[1]) * 62 + alphabet.find(s[2])*62*62 

def getBitNumber(id):
    if(id<0):
        print("can not get this bitnumber")
        exit(1)
    aux = 1
    while(id>0):
        aux = aux << 1
        id -= 1
    return aux

def base62(int, alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"):
    if int<62:
        return alphabet[int]
    else:
        return base62(int//62, alphabet) + alphabet[int % 62]



