import sqlite3

ebookstore = sqlite3.connect('ebookstore_db') 

cursor = ebookstore.cursor()

cursor.execute(''' 
CREATE TABLE ebookstore_db(id INTEGER PRIMARY KEY AUTOINCREMENT, Title TEXT, Author TEXT, Qty INTEGER) 
''')  # Creates table
ebookstore.commit() # Saves table

id1 = 3001
title1 = 'A Tale of Two Cities'
author1 = 'Charles Dickens'
qty1 = 30

id2 = 3002
title2 = 'Harry Potter and the Philosopher\'s Stone'
author2 = 'J.K. Rowling'
qty2 = 40

id3 = 3003
title3 = 'The Lion, the Witch and the Wardrobe'
author3 = 'C.S. Lewis'
qty3 = 25

id4 = 3004
title4 = 'The Lord of the Rings'
author4 = 'J.R.R Tolkien'
qty4 = 37

id5 = 3005
title5 = 'Alice in Wonderland'
author5 = 'Lewis Carroll'
qty5 = 12



# Adds books
books = [(id1,title1,author1,qty1),(id2,title2,author2,qty2),(id3,title3,author3,qty3),(id4,title4,author4,qty4),(id5,title5,author5,qty5)]
cursor.executemany(''' INSERT INTO ebookstore_db(id, Title, Author, Qty) VALUES(?,?,?,?)''', books)
ebookstore.commit() # Saves changes

ebookstore.close()