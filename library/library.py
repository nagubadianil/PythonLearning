from colorama import Fore
from colorama import Style

library = [{
    "title": "Book Title",
    "author": "Author Name",
    "editions": [
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
                "paperback": {"price": 12.99, "stock": 10},
                "eBook": {"price": 4.99, "stock": 200}
            }
        }
    ]
},{
    "title": "The One and Only",
    "author": "Me",
    "editions": [
        {
            "year": 2024,
            "formats": {
                "hardcover": {"price": 200.99, "stock": 1},
                "paperback": {"price": 120.99, "stock": 1},
                "eBook": {"price": 0, "stock": 1}
            }
        },
        {
            "year": 2015,
            "formats": {
                "hardcover": {"price": 18.99, "stock": 3},
                "paperback": {"price": 12.99, "stock": 10},
                "eBook": {"price": 4.99, "stock": 200}
            }
        }
    ]
}]

def returnmenu():
    input("----------\npress enter to return")
    
def displaymenu():
    print("\n----------Library----------")
    print("1.Edit inventory")
    print("2.View inventory")
    print("----------\n3.Exit")
    action=input("\nAction: ")
    return action

def search(place,book,charecteristic):
    i=0
    for b in place:
        if b[charecteristic]==book:
            return i
        else:
            i+=1
    return -1
            
def viewinv():
    print(f"{Fore.CYAN}----------View Inventory----------{Style.RESET_ALL}")
    print("1. View whole inventory")
    print("2. Search for a book")
    print("--------------------")
    viewaction=int(input("View: "))
    return viewaction

def viewwhleinv():
    for book in library:
        i=0
        print(f"""\n\033[32mBook Title: {book["title"]}
Author: {book["author"]}\033[0m""")
        for edition in book["editions"]:
            print("""----------Stock----------""")
            print(f"""Edition/Year: {edition["year"]}""")
            for format in book["editions"][i]["formats"]:
                print(f"""{format}: 
 Price: {book["editions"][i]["formats"][format]["price"]} 
 Stock: {book["editions"][i]["formats"][format]["stock"]}""")
            i+=1
    returnmenu()

def searchbook():
    book=input("Book title (no typos): ")
    bookid=search(library,book,"title")
    if bookid!=-1:
        print(f"""\n\033[32mBook Title: {library[bookid]["title"]}
        Author: {library[bookid]["author"]}\033[0m""")
        i=0
        for edition in library[bookid]["editions"]:
            print("""----------Stock----------""")
            print(f"""Edition/Year: {edition["year"]}""")
            for format in library[bookid]["editions"][i]["formats"]:
                if i==len(library[bookid]["editions"][i]["formats"]):
                    break
                else:
                    print(f"""{format}: 
        Price: {library[bookid]["editions"][i]["formats"][format]["price"]} 
        Stock: {library[bookid]["editions"][i]["formats"][format]["stock"]}""")
            i+=1
    else:
        print("Book doesnt exist")                     #it died try again
        
def editinv():
    print("\n----------Choose Editing----------")
    print("1.Add a book")
    print("2.Remove a book")
    print("3.Edit a book")
    editaction=input("\nEdit: ")
    return editaction

def addbook():
    title=input("\nTitle of the book: ")
    author=input(f"Author of {title}: ")
    year=input("Year of release: ")
    hardprice=input("Price of hardcover: ")
    hardstock=input("Stock of hardcovers: ")
    softprice=input("Price of softcover: ")
    softstock=input("Stock of softcovers: ")
    eprice=input("Price of ebook: ")
    estock=input("Stock of ebooks: ")
    newbook={
    "title": title,
    "author": author,
    "editions": [
        {
            "year": year,
            "formats": {
                "hardcover": {"price": hardprice, "stock": hardstock},
                "paperback": {"price": softprice, "stock": softstock},
                "eBook": {"price": eprice, "stock": estock}
            }
        }]}

    ifedi=input("""If there are no editions, press enter to add book.
To add editions, type 'add': """)
    if ifedi=="":
        library.append(newbook)
    elif ifedi=="add":
        newed=None
        ifmore=None
        while ifmore !="":
            eyear=input("Year of release: ")
            ehardprice=input("Price of hardcover: ")
            ehardstock=input("Stock of hardcovers: ")
            esoftprice=input("Price of softcover: ")
            esoftstock=input("Stock of softcovers: ")
            eeprice=input("Price of ebook: ")
            eestock=input("Stock of ebooks: ")
            newed={
            "year": eyear,
            "formats": {
                "hardcover": {"price": ehardprice, "stock": ehardstock},
                "paperback": {"price": esoftprice, "stock": esoftstock},
                "eBook": {"price": eeprice, "stock": eestock}
            }
        }
        
            newbook["editions"].append(newed)
            ifmore=input("""If no more editions are to be added, press enter to add book.
To add more editions, type 'add'""")
        library.append(newbook)
        
def removebook():
    i=0
    delbook=input("Input book name (no typos): ")
    for book in library:
        if book["title"]==delbook:
            confdel=input(f"Conrmation to delete {delbook} forever (A very long time!) (type yes or no): ")
            if confdel=="yes":
                library.pop(i)
            else:
                print("Confirmation denied")
                returnmenu()
        else:
            i+=1
            
def editbook():
    book=input("Book title (no typos): ")
    i=int(search(library,book,"title"))
    
    print("\n----------Edit a book----------")
    print("1.Update editions")
    print("2.Update author")
    print("3.Update date")
    return i

def uped():
    year=int(input("Year of release of edition: "))
    edition=search(library[bookindex]["editions"],year,"year")
    
    print("\n----------Edit a book----------")
    print("1.Update stock")
    print("2.Update price")
    print("3.Update date")
    return edition
    
def upstock():
    print(f"""----------Edit stock----------
1. Hardcover 
2. Softcover 
3. eBook """)
    stockaction=int(input("Edit which format: "))
    return stockaction

# def upprice():

# def upeddate():
    
# def upauth():
    
def update():
    print(f"Current date: ")
    date=input("")    
editaction=0
bookedit=0
action=0

while action!=3:
    action=int(displaymenu())
    if action==1:
        editaction=int(editinv())
        if editaction==1:
            addbook()
        elif editaction==2:
            removebook()
        elif editaction==3:
            bookindex=int(editbook())
            bookedit=int(input("Edit which characterestic: "))
            if bookedit==1:
                uped()
                edaction=int(input("Edit which characteristic: "))
                if edaction==1:
                    stockaction=upstock()
                    if stockaction==1:
                        uphardstock()
                    if stockaction==2:
                        upsoftstock()
                    if stockaction==3:    
                        upestock()
                if edaction==2:
                    priceaction=upprice()
                    
                    if priceaction==1:
                        uphardprice()
                    if priceaction==2:
                        upsoftprice()
                    if priceaction==3:
                        upeprice()
                if edaction==3:
                    upeddate()
            if bookedit==2:
                upauth()
            if bookedit==3:
                update()    
    elif action==2:
        viewaction=viewinv()
        if viewaction==1:
            viewwhleinv()
        if viewaction==2:
            searchbook()
          
         
        
    
    