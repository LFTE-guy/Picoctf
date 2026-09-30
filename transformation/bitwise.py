with open("enc","r") as F:
    A = F.read()

    for char in A :
        z = ord(char)
        d = chr(z >> 8)
        c = chr(z & 0x00FF) 
        print(d+c)
