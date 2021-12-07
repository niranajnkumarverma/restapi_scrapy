# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3 as sql
import pymysql as mysql


class QuotetutsPipeline:

    def __init__(self):
        self.del_db = "drop database if exists {}"
        self.del_tb = "drop table if exists quotes"
        self.create_db = "create database {} character set 'utf8'"
        self.create_tb = "create table quotes(title text, author text, tag text)"

        self.db_connect()
        self.create_database('quotes_db')
        self.create_table()

    def db_connect(self):
        # self.db = sql.connect("quote_spider.db")
        self.db = mysql.connect(host="localhost", port=3306, user="root", password="")

        self.cur = self.db.cursor()

    def create_database(self, db_name):
        self.cur.execute(self.del_db.format(db_name))
        self.cur.execute(self.create_db.format(db_name))  # command to create a new database
        self.db.select_db(db_name)  # select a database

    def create_table(self):
        self.cur.execute(self.del_tb)  # command to delete table if exists in database.
        self.cur.execute(self.create_tb)
        # self.db.commit()

    def insert(self, item):
        print('-------| insert method |-------')
        self.cur.execute(
            """insert into quotes values(%s,%s,%s)""",
            (item['title'][0][1:-1], str(item['author'][0]), str(item['tag'])[1:-1].replace("'", ""))
        )
        self.db.commit()  # commit make changes permanently

    def process_item(self, item, spider):
        # print("Pipeline item: ", item['title'][0], item['author'][0], item['tag'], sep="\n", )

        self.insert(item)
        return item
