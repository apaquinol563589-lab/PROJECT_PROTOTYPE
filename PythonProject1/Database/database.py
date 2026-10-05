import sqlite3
from pathlib import Path

class Database:

    def __init__(self, database_path=None):
        if database_path is None:
            database_path = Path(__file__).resolve().parent / "inventory.db"

        self.database_path = Path(database_path)
        self.create_tables()

    def connect(self):
        return sqlite3.connect(self.database_path)

    def create_tables(self):
        with self.connect() as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    price REAL NOT NULL,
                    category TEXT NOT NULL
                )
            """)

            connection.execute("""
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE
                )
            """)

            connection.execute("""
                INSERT OR IGNORE INTO categories (name)
                VALUES ('General')
            """)