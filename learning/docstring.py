class MyDocumentedClass:
    """This class is well documented but doesn't do anything special."""
    def do_nothing(self):
        """This method doesn't do anything but feel free to call it anyway."""
        pass

h = help(MyDocumentedClass)
print(h)

h = help(print)
print(h)

h= help(str.title)
print(h)

