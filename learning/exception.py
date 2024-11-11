try:
    print(2/0)
except ZeroDivisionError:
    print("You can't divide by zero!")
    
try:
    # Open file in read-only mode
    with open("not_here.txt", 'r') as f:
        f.write("Hello World!")
except IOError as e:
    print("An error occurred:", e)
finally: 
    print("Closing the file now")


class UserNotFoundError(Exception):
    pass
def fetch_user(user_id):
    # Here you would fetch from some kind of db, e.g.:
    # user = db.get_user(user_id)
    # To make this example runnable, let's set it to None
    user = None
    if user == None:
        raise UserNotFoundError(f'User {user_id} not in database')
    else:
        return user
users = [123, 456, 789]
for user_id in users:
    try:
        fetch_user(user_id)
    except UserNotFoundError as e:
        print("There was an error: ", e)