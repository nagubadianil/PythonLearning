list = [x for x in range(1,5)]
print (list)

list = [x for x in range(1,10) if x % 2 == 0]
print (list)

def some_function(a):
    return (a + 5) / 2
    
m = [some_function(x) for x in range(8)]
print(m)

# Nested list comprehension
m = [[j for j in range(3)] for i in range(4)]
print(m)

# if you want to flatten the previous matrix
v = [value for sublist in m for value in sublist]
print(v)

#set comprehension
s = {s for s in range(1,5) if s % 2}
print(s)

#dictionary comprehension
d = {x: x**2 for x in (2, 4, 6)}
print(d)