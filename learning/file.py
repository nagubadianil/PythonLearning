f = open('text.txt')
print(f.read())
f.close()

# By using Python’s with open(), the opened file resource will only 
# be available in the indented block of code:
with open('text.txt') as f:
    text = f.read()
print(text)

with open('test.txt', 'w') as f:
    for i in range(1, 5):
        f.write(str(i))

with open('test.txt', 'r') as f:
    print(f.read())
    
with open('test.txt', 'w') as f:
    for i in range(1, 5):
        f.write(f'Number {i}\n')

# Now add some extra lines using append mode
with open('test.txt', 'a') as f:
    for i in range(5, 8):
        f.write(f'Append number {i}\n')

with open('test.txt') as f:
    print(f.read())
    
with open('test.txt') as f:
    lines = f.readlines()

print(lines)