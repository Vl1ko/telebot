import sqlite3

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS "promo" (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        number text NOT NULL,
        amount integer NOT NULL
        )
        ''')

    def add_product(self, amount, number):
        with self.connection:
            for i in range(len(number)):
              self.cursor.execute("INSERT INTO 'promo' ('amount','number') VALUES (?, ?)", (amount, str(number[i]),))      

    def del_product(self, number):
        with self.connection:
            self.cursor.execute("DELETE FROM promo WHERE number = ?", (number,))

    def new_buy(self, amount):
        with self.connection:
            number = str(self.cursor.execute("SELECT number FROM promo WHERE amount = ?", (amount,)).fetchone()).split("'")[1]
            self.cursor.execute("DELETE FROM promo WHERE number = ?", (number,))
            return number

    def get_promo(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM promo").fetchall()
        
    def check_remain(self, amount):
        with self.connection:
            return len(self.cursor.execute("SELECT number FROM promo WHERE amount = ?", (amount,)).fetchall())

    def check_promo(self):
        with self.connection:
            if len(self.cursor.execute("SELECT * FROM promo").fetchall()) != 0:
                return True
            else:
                return False