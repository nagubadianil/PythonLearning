def myfunction():
    # This function has no body, which is not allowed
myfunction()

if True:
    # No code, not allowed!
else:
    # Here too, code is required
try:
    # let's try doing nothing (not allowed)
except Exception:
    # Again: this can't be empty!
class MyClass:
    # A completely empty class is not allowed

def myfunction():
    pass
myfunction()
if True:
    pass
else:
    pass
try:
    pass
except Exception:
    pass
class MyClass:
    pass

try:
    email = customer['email']
    send_notification(email, ...)
except KeyError:
    # Not the end of the world, let's continue
    pass

# We can use ... instead of pass
def create_account(username, password):
    # TODO: implement me
    ...