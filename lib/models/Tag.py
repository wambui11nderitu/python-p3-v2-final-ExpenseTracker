from lib.models.database import CURSOR, CONN

class Tag:
    def __init__(self, tag_id, name):
        self.tag_id = tag_id
        self.name = name

    def __repr__(self):
        return f"<Tag(tag_id={self.tag_id}, name='{self.name}')>"

    @classmethod
    def create(cls, name):
        CURSOR.execute('''
            INSERT INTO Tags (name)
            VALUES (?)
        ''', (name,))
        CONN.commit()
        return cls(CURSOR.lastrowid, name)

    @classmethod
    def get_all(cls):
        CURSOR.execute('SELECT * FROM Tags')
        tags = CURSOR.fetchall()
        return [cls(tag_id, name) for (tag_id, name) in tags]

    @classmethod
    def find_by_id(cls, tag_id):
        CURSOR.execute('SELECT * FROM Tags WHERE tag_id = ?', (tag_id,))
        tag = CURSOR.fetchone()
        if tag:
            return cls(*tag)
        return None

    @classmethod
    def delete(cls, tag_id):
        CURSOR.execute('DELETE FROM Tags WHERE tag_id = ?', (tag_id,))
        CONN.commit()

    @classmethod
    def add_tag_to_transaction(cls, transaction_id, tag_id):
        CURSOR.execute('''
            INSERT INTO TransactionTags (transaction_id, tag_id)
            VALUES (?, ?)
        ''', (transaction_id, tag_id))
        CONN.commit()

    @classmethod
    def get_tags_for_transaction(cls, transaction_id):
        CURSOR.execute('''
            SELECT Tags.tag_id, Tags.name FROM Tags
            JOIN TransactionTags ON Tags.tag_id = TransactionTags.tag_id
            WHERE TransactionTags.transaction_id = ?
        ''', (transaction_id,))
        tags = CURSOR.fetchall()
        return [cls(tag_id, name) for (tag_id, name) in tags]
