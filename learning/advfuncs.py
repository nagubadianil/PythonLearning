def f(*,a,b):
    print(a,b)

f (a=1,b=2)
args = { "a": 3, "b": 7}

f(**args)

def f (a, b, c):
    print(a,b,c)

listargs = [5,56,8]


f(*listargs)

def print_argument(func):
    def wrapper(the_number):
        print("Argument for", func.__name__, "is", the_number)
        return func(the_number)
    return wrapper
@print_argument
def add_one(x):
    return x + 1
print(add_one(1))

add_one = lambda x: x+1
print("result of lambda func", add_one(5))

numbers = [1, 2, 3, 4]
times_two = map(lambda x: x * 2, numbers)
print("result of map",list(times_two))
