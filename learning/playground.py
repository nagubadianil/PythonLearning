import sys
if len(sys.argv) == 2:
    name = sys.argv[1]
else:
    name = 'stranger'
print(f'Hi there, {name}')