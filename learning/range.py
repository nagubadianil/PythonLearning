r = range(5)
print(*r)

r = range(6,13)
print(*r)

r = range(2,10,3)
print(*r)

for i in range(0, 101, 10):
    print(i, end=" ")

print()

# range with negative step value
for i in range(5, 0, -1):
    print(i, end=" ")
    
print()

#test a number is in range
my_number = 10
print(my_number in range(0, 11))

#best way to convert a range to list
my_list = list(range(0, 3))
print(my_list)
# [0, 1, 2]