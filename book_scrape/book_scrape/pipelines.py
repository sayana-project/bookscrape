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

        # Table des genres (unique)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books_genres (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                genre TEXT UNIQUE
            )
        ''')

        # Table des livres avec clé étrangère genre_id
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                genre_id INTEGER,
                note INTEGER,
                stock_number INTEGER,
                datetime TEXT,
                upc TEXT,
                product_type TEXT,
                price_ht REAL,
                price_taxed REAL,
                review_number INTEGER,
                description TEXT,
                FOREIGN KEY(genre_id) REFERENCES books_genres(id)
            )
        ''')

    def process_item(self, item, spider):
        # Insérer le genre s’il n’existe pas
        self.cursor.execute('''
            INSERT OR IGNORE INTO books_genres (genre)
            VALUES (?)
        ''', (item['genre'],))

        # Récupérer l’ID du genre
        self.cursor.execute('SELECT id FROM books_genres WHERE genre = ?', (item['genre'],))
        genre_id = self.cursor.fetchone()[0]

        # Insérer le livre avec genre_id
        self.cursor.execute('''
            INSERT INTO books (title, genre_id, note, stock_number, datetime, upc, product_type, price_ht, price_taxed, review_number, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            item['title'],
            genre_id,
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
        self