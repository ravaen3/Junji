import randomIdPrototype

inputVar = input("what u wanna search\n type \"a\" for string to id\n type \"b\" for id to string\n")
if(inputVar=="a"): 
    aux =randomIdPrototype.reverseCharId(randomIdPrototype.reverseCharString(input("what you wanna search")))
    print(aux, "maps to", randomIdPrototype.getCharString(randomIdPrototype.getCharId(aux)))
elif inputVar=="b":
    number = int(input("type a number"))
    aux = randomIdPrototype.getCharString(randomIdPrototype.getCharId(number))
    print(aux, "maps to", randomIdPrototype.reverseCharId(randomIdPrototype.reverseCharString(aux)))
else: 
    print("type properly idiot")