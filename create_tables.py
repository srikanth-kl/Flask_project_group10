import sqlite3

conn = sqlite3.connect('database.db')
print("connection to the database success")

conn.execute('CREATE TABLE USER (UserName TEXT, email TEXT, userpwd TEXT, mobileNumber INTEGER)')
print("User table created")

conn.execute('')

conn.close()