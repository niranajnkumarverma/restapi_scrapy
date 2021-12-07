# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector


class ScrapytutorialPipeline:
    def __init__(self):
        print("-------------init called------")
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            port=3306,
            user = "root",
            password = "",
            database = "myquotes_mysql_db"
        )

        self.curr = self.conn.cursor()

    def create_table(self):
        # self.curr.execute("""drop table if exists quotes_mysql_tb""")
        self.curr.execute("""create table quotes_mysql_tb(title text, author text, tage text)""")

    def store_db(self,item):
        self.curr.execute("""insert into quotes_mysql_tb value(%s,%s,%s)""",(
            item["title"][0],
            item["author"][0],
            item["tage"][0]

        ))
        self.conn.commit()

    def process_item(self,item,spider):
        self.store_db(item)
        return item





