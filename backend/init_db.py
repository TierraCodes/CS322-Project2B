import sqlite3

# connect to the database (if file does not exist -- create it)
connection = sqlite3.connect('database.db')

# open the schema.sql file which describes the database
with open('schema.sql') as db_file:
    # run the commands in this file
    connection.executescript(db_file.read())

# connect to the database with a cursor
cur = connection.cursor()

# add two default entries
# TODO: You will need to modify this to handle the additional fields
cur.execute("INSERT INTO destinations (destination, notes, cost) VALUES (?, ?, ?)",
            ('Hawaii', 'honolulu', 35.45)
            )
cur.execute("INSERT INTO destinations (destination, notes, cost) VALUES (?, ?, ?)",
            ('Bahamas', 'nassau', 99.49)
            )

# commit changes and close the connection
connection.commit()
connection.close()