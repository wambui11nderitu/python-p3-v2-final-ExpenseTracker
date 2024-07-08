from lib.models.database import CURSOR, CONN
from lib.models.Tag import Tag

class Transaction:
    def __init__(self, transaction_id, amount, date, category_id, description):
        self.transaction_id = transaction_id
        self.amount = amount
        self.date = date
        self.category_id = category_id
        self.description = description

    def __repr__(self):
        return f"<Transaction(transaction_id={self.transaction_id}, amount={self.amount}, date='{self.date}', category_id={self.category_id}, description='{self.description}')>"

    @classmethod
    def create(cls, amount, date, category_id, description):
        CURSOR.execute('''
            INSERT INTO Transactions (amount, date, category_id, description)
            VALUES (?, ?, ?, ?)
        ''', (amount, date, category_id, description))
        CONN.commit()
        return cls(CURSOR.lastrowid, amount, date, category_id, description)

    @classmethod
    def get_all(cls):
        CURSOR.execute('SELECT * FROM Transactions')
        transactions = CURSOR.fetchall()
        return [cls(transaction_id, amount, date, category_id, description) for (transaction_id, amount, date, category_id, description) in transactions]

    @classmethod
    def find_by_id(cls, transaction_id):
        CURSOR.execute('SELECT * FROM Transactions WHERE transaction_id = ?', (transaction_id,))
        transaction = CURSOR.fetchone()
        if transaction:
            return cls(*transaction)
        return None

    @classmethod
    def delete(cls, transaction_id):
        CURSOR.execute('DELETE FROM Transactions WHERE transaction_id = ?', (transaction_id,))
        CONN.commit()

    def add_tag(self, tag_id):
        Tag.add_tag_to_transaction(self.transaction_id, tag_id)

    def get_tags(self):
        return Tag.get_tags_for_transaction(self.transaction_id)


