import sqlite3 as sql

db = sql.connect("quote_spider.db")

cur = db.cursor()

create_tb = "create table quotes(title, author, tag)"
insert_data = "insert into quotes values()"
try:
    cur.execute(create_tb)
except Exception as err:
    print("Error: ", err)

db.commit()

db.close()
