from Database.database import Database
from .model import Category


class CategoryRepository:

    def __init__(self, database: Database):
        self.database = database

    def get_categories(self):
        with self.database.connect() as connection:
            rows = connection.execute(
                "SELECT id, name FROM categories ORDER BY name"
            ).fetchall()

        return [
            Category(row[1])
            for row in rows
        ]

    def get_category(self, name):
        with self.database.connect() as connection:
            row = connection.execute(
                """
                SELECT name
                FROM categories
                WHERE lower(name) = lower(?)
                """,
                (name,)
            ).fetchone()

        return Category(row[0]) if row else None

    def category_exists(self, name):
        return self.get_category(name) is not None

    def add_category(self, category):
        with self.database.connect() as connection:
            connection.execute(
                "INSERT INTO categories (name) VALUES (?)",
                (category.name,)
            )

    def delete_category(self, name):
        with self.database.connect() as connection:
            connection.execute(
                """
                DELETE FROM categories
                WHERE lower(name) = lower(?)
                """,
                (name,)
            )