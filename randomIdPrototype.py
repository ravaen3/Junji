



def getCharId(id):
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    aux = 0
    size = 17 #size is the floor(2log(len(alphabet)))
    for i in range(0,size):
        aux *=2
        aux = aux + ( 1 if getBitNumber(13*i % size) & id > 0 else 0)

    return aux
    return (alphabet[aux & (getBitNumber(6)-1)] + alphabet[aux>>5 & (getBitNumber(6)-1)] + alphabet[aux >>10 & (getBitNumber(6)-1)])

def reverseCharId(id):
    size = 17 #size is the floor(2log(len(alphabet)))
    aux = 0
    idcopy = id
    for i in range(0, size):
        if(idcopy & 1 > 0):
            aux = aux + getBitNumber(13*(size-i-1) % size)
        idcopy = idcopy >> 1
    return aux


def getCharString(id):
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

    return (alphabet[id % 62] + alphabet[id//62  % 62] + alphabet[id//62//62  % 62])

def reverseCharString(s):
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
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

for i in range(0, 100):
    aux = getCharId(i)
    s = getCharString(aux)
    sr = reverseCharString(s)


    print(i, aux, reverseCharId(aux), s, sr, reverseCharId(sr))