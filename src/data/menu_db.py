import sqlite3
from typing import List, Dict

class MenuDatabase:
    def __init__(self, db_file: str = "menu.db"):
        self.db_file = db_file
        self._create_table()

    def _create_table(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS menu_items (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            category TEXT NOT NULL
        )
        ''')
        conn.commit()
        conn.close()

    def add_item(self, name: str, description: str, price: float, category: str):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO menu_items (name, description, price, category) VALUES (?, ?, ?, ?)',
                       (name, description, price, category))
        conn.commit()
        conn.close()

    def get_all_items(self) -> List[Dict]:
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM menu_items')
        items = cursor.fetchall()
        conn.close()
        return [{'id': item[0], 'name': item[1], 'description': item[2], 'price': item[3], 'category': item[4]} for item in items]

    def get_item_by_name(self, name: str) -> Dict:
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM menu_items WHERE name = ?', (name,))
        item = cursor.fetchone()
        conn.close()
        return {'id': item[0], 'name': item[1], 'description': item[2], 'price': item[3], 'category': item[4]} if item else None

    def get_item_by_id(self, id: int) -> Dict:
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM menu_items WHERE id = ?', (id,))
        item = cursor.fetchone()
        conn.close()
        return {'id': item[0], 'name': item[1], 'description': item[2], 'price': item[3], 'category': item[4]} if item else None

    def update_item(self, id: int, name: str, description: str, price: float, category: str):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('UPDATE menu_items SET name = ?, description = ?, price = ?, category = ? WHERE id = ?',
                       (name, description, price, category, id))
        conn.commit()
        conn.close()

    def delete_item(self, id: int):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM menu_items WHERE id = ?', (id,))
        conn.commit()
        conn.close()

