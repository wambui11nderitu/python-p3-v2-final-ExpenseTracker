import sqlite3

CONN = sqlite3.connect('company.db')
CURSOR = CONN.cursor()

def initialize_db():
    # Check if the tables already exist
    tables = ["Transactions", "Budgets", "Categories"]
    existing_tables = []
    
    for table in tables:
        CURSOR.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
        if CURSOR.fetchone():
            existing_tables.append(table)
    
    if "Transactions" not in existing_tables:
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
        
    if "Budgets" not in existing_tables:
        CURSOR.execute('''
        CREATE TABLE IF NOT EXISTS Budgets (
            budget_id INTEGER PRIMARY KEY,
            category_id INTEGER,
            budget_limit REAL NOT NULL,
            FOREIGN KEY (category_id) REFERENCES Categories(category_id)
        )
        ''')
        
    if "Categories" not in existing_tables:
        CURSOR.execute('''
        CREATE TABLE IF NOT EXISTS Categories (
            category_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL
        )
        ''')

    CONN.commit()

if __name__ == '__main__':
    initialize_db()
    print("Database initialized")

