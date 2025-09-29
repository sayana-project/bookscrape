# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import sqlite3

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class SQLitePipeline:
    def open_spider(self, spider):
        self.conn = sqlite3.connect('books.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                title TEXT,
                genre TEXT,
                note INTEGER,
                stock_number INTEGER,
                datetime TEXT,
                upc TEXT,
                product_type TEXT,
                price_ht REAL,
                price_taxed REAL,
                review_number INTEGER,
                description TEXT
            )
        ''')

    def process_item(self, item, spider):
        self.cursor.execute('''
            INSERT INTO books VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            item['title'],
            item['genre'],
            item['note'],
            int(item['stock_number']),
            item['datetime'],
            item['upc'],
            item['product_type'],
            float(item['price_ht']),
            float(item['price_taxed']),
            int(item['review_number']),
            item['description']
        ))
        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.conn.close()