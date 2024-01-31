import randomIdPrototype
import random

def base62(int, alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"):
    if int<62:
        return alphabet[int]
    else:
        return base62(int//62, alphabet) + alphabet[int % 62]

for i in range(10000, 11000):
    aux = randomIdPrototype.getCharId(i)
    s = randomIdPrototype.getCharString(aux)
    sr = randomIdPrototype.reverseCharString(s)


    print(i, aux, randomIdPrototype.reverseCharId(aux), s, sr, randomIdPrototype.reverseCharId(sr))
    print("Ravaen:", base62(i), ", Daisey:", s)
    print()


low = 1
while(low < 2**32):
    x = random.randrange(low, low+1000)
    cid = randomIdPrototype.getCharId(x)
    if(randomIdPrototype.reverseCharId(cid)!=x):
        print("error, x=", x, " exiting now")
        exit(1)
    low+=100000
print("success")

