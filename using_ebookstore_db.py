import sqlite3

ebookstore = sqlite3.connect('ebookstore_db') # Connects to ebookstore_db

cursor = ebookstore.cursor() # Creates cursor object

def enter_book(title, author, qty): # Function for adding new books to the database
   
    cursor.execute('''INSERT INTO ebookstore_db(Title, Author, Qty) 
    VALUES(?,?,?)''', (title, author, qty)) # Adds the new book to the database, id should be added automatically

    ebookstore.commit() # Saves changes

    print(f'\n{title} by {author} has been added to the database:\n{search_book(title, author, None)}') # Confirms the book has been added and displays its row

def update_book(title, author, id): # Function for updating an existing book
    
    menu_bool = True

    while menu_bool: # Repeats the request for a choice until the user makes a valid one by entering 1, 2, or 3
        choice = input('''
    1. Title
    2. Author
    3. Qty

    Which column would you like to update? ''') 
        # The following block of if/elif/else statements activate depending on the user's choice in the above menu
        # By selecting an option from the menu, the user indicates they wish to edit that column
        # (The user has already selected the row in the main body of code) 
        # The name of the column they have chosen to edit is stored in 'column' variable
        # The value they wish to change the existing value to is stored in the 'new column' variable
        # The menu_bool is set to False to exit the while loop for this process
        # The 'column' variable, combined with the row identifier the user already entered, is used to located the cell for updating
        # Once located, the cell's value is replaced with the value stored in 'new_value'

        if choice == '1': # Assigns values to variables for a title change

            column = 'Title'
            new_value = input('\nEnter the new title: ')
            menu_bool = False

        elif choice == '2': # Assigns values to variables for an author change

            column = 'Author'
            new_value = input('\nEnter the new author: ')
            menu_bool = False

        elif choice == '3': # Assigns values to variables for a qty change

            column = 'Qty'
            y = 'Please enter the new quantity'
            new_value = is_int(y) # Gets the new quantity from the user, ensuring a number has been entered
            menu_bool = False

        else:
            print('\nPlease enter a valid choice.') # Continues while loop
        
    if title == None and author == None:

        cursor.execute(f'''UPDATE ebookstore_db SET {column} = ? WHERE id = ? ''', (new_value, id,)) # Updates the desired entry by id
        print(f'\nBook {id}\'s {column} has been updated.')

    else:

        cursor.execute(f'''UPDATE ebookstore_db SET {column} = ? WHERE title = ? AND author = ? ''', (new_value, title, author,)) # Updates the desired entry by Title and Author
        print(f'\n{title}\'s {column} has been updated.')

    ebookstore.commit()

def delete_book(title, author, id): # Function for deleting a book by id or a combination of title and author

    if title == None and author == None: # Determins how the book will be named in the 'Are you sure' question
        name = f'book {id}'
    else:
        name = title

    sure_bool = True

    while sure_bool: # While loop for confirmation of book deletion, loops until user enters yes or no

        sure = input(f'\nAre you sure you wish to delete {name} from the database? yes/no ')

        if sure.lower() == 'yes':
            
            if  title == None and author == None: # Deletes the book by id

                cursor.execute('''DELETE FROM ebookstore_db WHERE id = ? ''', (id,)) # Deletes specified book
                ebookstore.commit() # Saves changes
                print(f'\nBook {id} has been deleted.')
                sure_bool = False

            else: # Deletes the book by title and author

                cursor.execute('''DELETE FROM ebookstore_db WHERE title = ? AND author = ?''', (title, author,)) # Deletes specified book
                ebookstore.commit() # Saves changes
                print(f'\n{title} has been deleted.')
                sure_bool = False

        elif sure.lower() == 'no':

            print('\nNo changes made.')
            sure_bool = False

        else:
            print('\nPlease enter a valid choice.')
            
def search_book(title, author, id): # Searches books based on id or a combination of title and author

    if title == None and author == None:
        cursor.execute('''SELECT id, Title, Author, Qty FROM ebookstore_db WHERE id = ?
    ''', (id,))
    elif id == None:
        cursor.execute('''SELECT id, Title, Author, Qty FROM ebookstore_db WHERE title = ? AND author = ?
    ''', (title, author,))

    book = cursor.fetchone()
    return book

def is_int(x): # Function for checking a number has been entered and returning the user input as an integer
   
    int_bool = True

    while int_bool: # Loops until an integer has been entered
        
        y = input(f'{x}: ')

        try:
            y = int(y)
            int_bool = False
            return y
            
        except:
            print(f'\nPlease enter a number.\n')

def title_or_id(x): # Function for assigning the variables (title, author, id) used to search by id or a combination of title and author
    
    z = x.lower() # Changes x to lower case for use in sentences
    choice_bool = True
    while choice_bool: # Loops until a valid answer is given to the 'by id?' question

        choice = input(f'\n{x} by id? yes/no, or type \'c\' to cancel: ')
        
        if choice.lower() == 'yes': # Assigns variables so book can be searched by id

            title = None
            author = None

            search_bool = True
            while search_bool: # Loops until user enters a valid id

                y = '\nEnter book id' # Assings variable for the is_int() function
                id = is_int(y) # Calls function to prompt user for id and ensure a number is returned

                if search_book(title, author, id) == None: # Checks if id is in database
                    print(f'\nBook with id {id} not found in database. Please try again.')
                else:
                    print('\n')
                    print(search_book(title, author, id))
                    search_bool = False # Exits while loop

            choice_bool = False # Exits while loop
            return [title, author, id]
        
        elif choice.lower() == 'no': # Assigns variables so book can be searched by title and author

            id = None

            search_bool = True
            while search_bool:

                title = input(f'\nEnter the title of the book you wish to {z}, or type \'c\' to cancel: ')
                
                if title.lower() == 'c':
                    return 'cancel'
                
                else:

                    author = input(f'\nEnter the author of the book you wish to {z}, or type \'c\' to cancel: ')
                
                    if author.lower() == 'c':
                        return 'cancel'

                    else:
                        if search_book(title, author, id) == None: # Checks if title/author is in database
                            print(f'\n{title} by {author} not found in database. Please try again.\n')
                        else:
                            search_bool = False

            choice_bool = False # Exits while loop
            return [title, author, id]

        elif choice.lower() == 'c':
            return 'cancel'

        else: 
            print('\n Please enter yes or no.\n')

user_input = ':)' # Initialises the 'user_input' variable as not '0', allowing the following while loop to start. 'user_input' is then reassigned as the user's input within the while loop.

while user_input != '0': # Program will end when 0 is entered
    
    print('''
1. Enter book
2. Update book
3. Delete book
4. Search books
5. Display all books
0. Exit''')

    user_input = input('\nEnter the number corresponding to the opperation you wish to perform: ')

    if user_input == '1': # If the user selects 'Enter book'

        title = input('Title: ')
        author = input('Author: ')
        x = 'Qty' # Assigns variable required for is_int() function
        qty = is_int(x) # Calls function to prompt user for Qty and ensure a number is returned

        enter_book(title,author,qty) # Uses the enter_book function to add the new book to the database

    elif user_input == '2': # If the user selects 'Update book'

        x = 'Select for updates' # Assigns variable for the title_or_id() function
        tai_list = title_or_id(x) # List containing values for title, author, and list, retrieved from the user by the title_or_id function
        
        if tai_list == 'cancel':
           
            continue

        else:
            title = tai_list[0]
            author = tai_list[1]
            id = tai_list[2]

            update_book(title, author, id) # Uses the update_book function to update the database

    elif user_input == '3': # If the user selects 'Delete book'

        w = 'Delete' # Assigns variable for the 'title_or_id' function

        tai_list = title_or_id(w) # List containing values for title, author, and list, retrieved from the user by the title_or_id function

        if tai_list == 'cancel':
            
            continue

        else:
            title = tai_list[0]
            author = tai_list[1]
            id = tai_list[2]
    
            delete_book(title, author, id) # Uses the delete book function to delete a specified row
        
    elif user_input == '4': # If user selects 'Search book'

        x = 'Search' # Assigns variable for the 'title_or_id' function

        title_or_id(x) # List containing values for title, author, and list, retrieved from the user by the title_or_id function
        # The searched for row is printed as part of the title_or_id function
       
        if title_or_id(x) == 'cancel':
            continue

    elif user_input == '5': # If user selects 'Display all books'
        
        print('\n(id,    Title,    Author,    Qty)') 
        for row in cursor.execute('SELECT * FROM ebookstore_db;'):
            print(row)
    
    elif user_input == '0': # When user selects 'Exit'
        
        print('\nGoodbye')
        ebookstore.close()
    
    else:
        print('\nPlease enter one of the options provided.')