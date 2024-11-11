my_iterable = range(1, 3)
my_iterator = my_iterable.__iter__()
v = my_iterator.__next__()
print(v)
v = my_iterator.__next__()
print(v)


# iterating over dictionary
d = {'name': 'Alice', 'age': 23, 'country': 'NL' }
for k,v in d.items():
     print(k, v)
     
#build your own iterable and iterator
class EvenNumbers:
    last = 0
    def __iter__(self):
        return self
    def __next__(self):
        self.last += 2
        if self.last > 8:
            raise StopIteration
        return self.last
even_numbers = EvenNumbers()
for num in even_numbers:
    print(num)