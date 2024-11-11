# Inventory array to store books
inventory = []

# Function to add a book with multiple editions
def add_book(inventory, title, author, editions):
    book = {
        "title": title,
        "author": author,
        "editions": editions
    }
    inventory.append(book)

# Function to update price or stock of a format in a specific edition
def update_format(inventory, title, year, format_type, new_price=None, new_stock=None):
    for book in inventory:
        if book['title'] == title:
            for edition in book['editions']:
                if edition['year'] == year:
                    if format_type in edition['formats']:
                        if new_price is not None:
                            edition['formats'][format_type]['price'] = new_price
                        if new_stock is not None:
                            edition['formats'][format_type]['stock'] = new_stock
                        return
    print(f"Edition of '{title}' from year {year} not found or format {format_type} not available.")

# Function to remove a specific edition
def remove_edition(inventory, title, year):
    for book in inventory:
        if book['title'] == title:
            for i, edition in enumerate(book['editions']):
                if edition['year'] == year:
                    del book['editions'][i]
                    return
    print(f"Edition of '{title}' from year {year} not found.")

# Function to print the inventory
def print_inventory(inventory):
    for book in inventory:
        print(f"Title: {book['title']}, Author: {book['author']}")
        for edition in book['editions']:
            print(f"  Edition Year: {edition['year']}")
            for format_type, details in edition['formats'].items():
                print(f"    Format: {format_type}, Price: {details['price']}, Stock: {details['stock']}")

# Function to sort books by title or author
def sort_books(inventory, by="title"):
    inventory.sort(key=lambda book: book[by])

# Function to sort editions by year
def sort_editions(book):
    book['editions'].sort(key=lambda edition: edition['year'])

# Function to reverse editions and formats
def reverse_editions_and_formats(book):
    book['editions'].reverse()
    for edition in book['editions']:
        edition['formats'] = dict(reversed(list(edition['formats'].items())))

# Shallow and deep copy demonstration
import copy
def shallow_copy_book(book):
    return book.copy()

def deep_copy_book(book):
    return copy.deepcopy(book)

# Function to find the book with the highest overall value (price * stock for all editions and formats)
def find_highest_value_book(inventory):
    highest_value = 0
    highest_value_book = None
    for book in inventory:
        total_value = sum(details['price'] * details['stock']
                          for edition in book['editions']
                          for details in edition['formats'].values())
        if total_value > highest_value:
            highest_value = total_value
            highest_value_book = book
    return highest_value_book

# Function to calculate total number of books in the inventory
def calculate_total_stock(inventory):
    total_stock = sum(details['stock']
                      for book in inventory
                      for edition in book['editions']
                      for details in edition['formats'].values())
    return total_stock

# Test the functions
editions = [
    {
        "year": 2020,
        "formats": {
            "hardcover": {"price": 20.99, "stock": 5},
            "paperback": {"price": 12.99, "stock": 10},
            "eBook": {"price": 5.99, "stock": 100}
        }
    },
    {
        "year": 2015,
        "formats": {
            "hardcover": {"price": 18.99, "stock": 3},
            "eBook": {"price": 4.99, "stock": 200}
        }
    }
]


# Add a book
add_book(inventory, "The Great Gatsby", "F. Scott Fitzgerald", editions)

# Print the inventory
print("Initial Inventory:")
print_inventory(inventory)

# Update the stock of a format in a specific edition
update_format(inventory, "The Great Gatsby", 2020, "paperback", new_stock=12)

# Sort books by title
sort_books(inventory, by="title")

# Sort editions of a book by year
sort_editions(inventory[0])

# Reverse editions and formats for a book
reverse_editions_and_formats(inventory[0])

# Demonstrate shallow and deep copy
shallow_copied_book = shallow_copy_book(inventory[0])
deep_copied_book = deep_copy_book(inventory[0])

# Print the inventory after operations
print("\nUpdated Inventory:")
print_inventory(inventory)

# Find the highest value book
highest_value_book = find_highest_value_book(inventory)
print(f"\nBook with the highest value: {highest_value_book['title']}")

# Calculate total stock of books
total_stock = calculate_total_stock(inventory)
print(f"\nTotal stock of books in inventory: {total_stock}")

# Function to display menu options
def display_menu():
    print("\nBookstore Inventory Management")
    print("1. Add a book")
    print("2. Update stock")
    print("3. Sort books")
    print("4. Find highest value book")
    print("5. Calculate total stock")
    print("6. Print inventory")
    print("7. Exit")

# Function to get user input for adding a book
def get_book_input():
    title = input("Enter book title: ")
    author = input("Enter author name: ")
    editions = []
    while True:
        year = input("Enter edition year (or press Enter to finish): ")
        if not year:
            break
        year = int(year)
        formats = {}
        while True:
            format_type = input("Enter format type (or press Enter to finish): ")
            if not format_type:
                break
            price = float(input(f"Enter price for {format_type}: "))
            stock = int(input(f"Enter stock for {format_type}: "))
            formats[format_type] = {"price": price, "stock": stock}
        editions.append({"year": year, "formats": formats})
    return title, author, editions

# Main loop for user interaction
while True:
    display_menu()
    choice = input("Enter your choice (1-7): ")

    if choice == '1':
        title, author, editions = get_book_input()
        add_book(inventory, title, author, editions)
        print("Book added successfully!")

    elif choice == '2':
        title = input("Enter book title: ")
        year = int(input("Enter edition year: "))
        format_type = input("Enter format type: ")
        new_stock = int(input("Enter new stock: "))
        update_format(inventory, title, year, format_type, new_stock)
        print("Stock updated successfully!")

    elif choice == '3':
        sort_by = input("Sort by 'title' or 'author': ")
        sort_books(inventory, by=sort_by)
        print("Books sorted successfully!")

    elif choice == '4':
         
        highest_value_book = find_highest_value_book(inventory)
        total_value = sum(details['price'] * details['stock']
                          for edition in highest_value_book['editions']
                          for details in edition['formats'].values())
        print(f"Book with the highest value: {highest_value_book['title']}")
        print(f"Total value: ${total_value:.2f}")

    elif choice == '5':
        total_stock = calculate_total_stock(inventory)
        print(f"Total stock of books in inventory: {total_stock}")

    elif choice == '6':
        print_inventory(inventory)

    elif choice == '7':
        print("Exiting the program. Goodbye!")
        break

    else:
        print("Invalid choice. Please try again.")

# Note: The following lines are being commented out as they are now handled by the menu system
# print("\nUpdated Inventory:")
# print_inventory(inventory)
# highest_value_book = find_highest_value_book(inventory)
# print(f"\nBook with the highest value: {highest_value_book['title']}")
# total_stock = calculate_total_stock(inventory)
# print(f"\nTotal stock of books in inventory: {total_stock}")

