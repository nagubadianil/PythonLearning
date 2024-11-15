#  y o o o o o o o o
# decorator is a function wrapper
# or is it a rapper?
# the outer function is cal#  y o o o o o o o o
# decorator is a function wrapper
# or is it a rapper?
# the outer function is called the decorator which takes the original function as an argument and returns a modified version
import colorama
from colorama import Fore
from colorama import Style


def italicizeme():
    def italicizeme_func(myfunc):
        def wrapper(*args, **kwargs):
            # Call the original function and get its result
            print(f"\033[3m", end="")
            myfunc(*args,**kwargs)
            print(f"\033[0m", end="")
        return wrapper
    return italicizeme_func

def underlineme():
    def underlineme_func(myfunc):
        def wrapper(*args, **kwargs):
            # Call the original function and get its result
            print(f"\033[4m", end="")
            myfunc(*args,**kwargs)
            print(f"\033[0m", end="")
        return wrapper
    return underlineme_func

def boldme():
    def boldme_func(myfunc):
        def wrapper(*args, **kwargs):
            # Call the original function and get its result
            print(f"\033[1m", end="")
            myfunc(*args,**kwargs)
            print(f"\033[0m", end="")
        return wrapper
    return boldme_func

def colorizeme(color):
    def colorizeme_func(myfunc):
        def wrapper(*args, **kwargs):
            # Call the original function and get its result
            print(f"{color}", end="")
            myfunc(*args,**kwargs)
            print(f"{Style.RESET_ALL}", end="")
        return wrapper
    return colorizeme_func

@boldme()
@colorizeme(Fore.MAGENTA)
def print_bm(*args,**kwargs):
    print(*args,**kwargs,end="")

@italicizeme()
@colorizeme(Fore.YELLOW)
def print_iy(*args,**kwargs):
    print(*args,**kwargs,end="")



@colorizeme(Fore.LIGHTBLUE_EX)
def print_lb(*args,**kwargs):
    print(*args,**kwargs,end="")

@underlineme()
@colorizeme(Fore.CYAN)
def print_uc(*args,**kwargs):
    print(*args,**kwargs,end="")


print_bm("My") 
print_iy(" name")
print_lb(" is")
print_uc(" Bhavesh")
print("\n", end="")
print_lb("I" )
print_bm(" am a") 
print_uc(" 10th grade")
print_iy(" Student!")




 

















