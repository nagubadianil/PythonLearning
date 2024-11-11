
print(dir())
print("-"*100)
my_list = [1,3,4,5]
print([item for item in dir(my_list) if not item.startswith('__')])
print("-"*100)
print(locals())
print("-"*100)
print(dir(locals()['__builtins__']))
print("-"*100)
print(globals() )
print("-"*100)
print(vars(my_list))