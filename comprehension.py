print("basic iteration 2-5:", [i for i in range(2, 5)])
print("basic iteration 1-6:", [j for j in range(1, 6)])
multiplication = [[i * j for j in range(1, 6)] for i in range(2, 5)]

print("Matrice with multiplication of above two:", multiplication)
pairings = [(i , j) for j in range(1, 6) for i in range(2, 5)]
print("Pairings: ", pairings)

print("Dictionary 2-5:",{"name_"+str(i):i for i in range(2, 5)})

