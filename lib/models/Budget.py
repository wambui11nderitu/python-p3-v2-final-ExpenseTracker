import sqlite3
from lib.models import CONN, CURSOR

class Budget:
    def __init__(self, budget_id, category_id, budget_limit):
        self.budget_id = budget_id
        self.category_id = category_id
        self.budget_limit = budget_limit

    @classmethod
    def create(cls, category_id, budget_limit):
        CURSOR.execute('''
            INSERT INTO Budgets (category_id, budget_limit)
            VALUES (?, ?)
        ''', (category_id, budget_limit))
        CONN.commit()
        return cls(CURSOR.lastrowid, category_id, budget_limit)

    @classmethod
    def get_all(cls):
        CURSOR.execute('SELECT * FROM Budgets')
        rows = CURSOR.fetchall()
        return [cls(*row) for row in rows]

    @classmethod
    def find_by_id(cls, budget_id):
        CURSOR.execute('SELECT * FROM Budgets WHERE budget_id = ?', (budget_id,))
        row = CURSOR.fetchone()
        if row:
            return cls(*row)
        return None

    def update(self, category_id, budget_limit):
        CURSOR.execute('''
            UPDATE Budgets
            SET category_id = ?, budget_limit = ?
            WHERE budget_id = ?
        ''', (category_id, budget_limit, self.budget_id))
        CONN.commit()
        self.category_id = category_id
        self.budget_limit = budget_limit

    def delete(self):
        CURSOR.execute('DELETE FROM Budgets WHERE budget_id = ?', (self.budget_id,))
        CONN.commit()

    def __repr__(self):
        return f"Budget(budget_id={self.budget_id}, category_id={self.category_id}, budget_limit={self.budget_limit})"
