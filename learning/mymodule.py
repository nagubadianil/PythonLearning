def my_function():
    print('Hello Rushi')

# Print out my name when called as script
# If not print out the name of module

if __name__ == "__main__":
    print("This is script. My name is Rushi!")
else:
    print("We are running it as a module:", __name__)