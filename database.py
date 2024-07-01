import sqlite3


class DatabaseManager:
    def __init__(self, db_name='products.db'):
        self.db_name = db_name

    def init_db(self):
        """
        Initializes the database
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            link TEXT UNIQUE,
                            price INTEGER,
                            brand TEXT
                        )''')
        conn.commit()
        conn.close()

    def save_new_items(self, items, max_items):
        """
        Saves new items that are scraped to the database
        """
        new_items = []
        if len(items) < max_items:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                for item in items:
                    cursor.execute("SELECT 1 FROM products WHERE link = ?", (item["link"],))
                    if not cursor.fetchone():
                        cursor.execute("INSERT INTO products (link, price, brand) VALUES (?, ?, ?)",
                                       (item["link"], item["price"], item["brand"]))
                        new_items.append(item)
                conn.commit()
        return new_items

    def clear_database(self):
        """
        Clear the database by dropping the table products
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS products')
        conn.commit()
        conn.close()
