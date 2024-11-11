inc=0
numb=0
try:
    while numb!="exit":
        numb=int(input("numebr: "))
        if numb==inc+1:
            inc+=1
        else:
            print("wrong try again")
            break
except ValueError:
    print("Value error")