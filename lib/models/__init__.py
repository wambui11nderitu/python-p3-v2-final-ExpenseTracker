import sqlite3
from .Category import Category

CONN = sqlite3.connect('company.db')
CURSOR = CONN.cursor()

def initialize_db():
    CURSOR.execute('''
    CREATE TABLE IF NOT EXISTS Transactions (
        transaction_id INTEGER PRIMARY KEY,
        amount REAL NOT NULL,
        date TEXT NOT NULL,
        category_id INTEGER,
        description TEXT,
        FOREIGN KEY (category_id) REFERENCES Categories(category_id)
    )
    ''')
    
    CURSOR.execute('''
    CREATE TABLE IF NOT EXISTS Budget (
        budget_id INTEGER PRIMARY KEY,
        category_id INTEGER,
        budget_limit REAL NOT NULL,
        FOREIGN KEY (category_id) REFERENCES Categories(category_id)
    )
    ''')
    
    CURSOR.execute('''
    CREATE TABLE IF NOT EXISTS Categories (
        category_id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL
    )
    ''')
    
    CURSOR.execute('''
    CREATE TABLE IF NOT EXISTS Tags (
        tag_id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL
    )
    ''')

    CURSOR.execute('''
    CREATE TABLE IF NOT EXISTS TransactionTags (
        transaction_id INTEGER,
        tag_id INTEGER,
        PRIMARY KEY (transaction_id, tag_id),
        FOREIGN KEY (transaction_id) REFERENCES Transactions(transaction_id),
        FOREIGN KEY (tag_id) REFERENCES Tags(tag_id)
    )
    ''')

    CONN.commit()

if __name__ == '__main__':
    initialize_db()
    print("Database initialized")




