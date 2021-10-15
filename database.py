import sqlite3
conn = sqlite3.connect("inter.db")
sql="CREATE TABLE Processors(name TEXT, brand TEXT, price INTEGER, description TEXT, photo_link TEXT, product_link TEXT)"
cursor = conn.cursor()
cursor.execute(sql)
conn.close()