from Database.database import Database
from .model import Item

class ManagementRepository:

    def __init__(self, database: Database):
        self.database = database

    def get_items(self):
        with self.database.connect() as connection:
            rows = connection.execute(
                "SELECT id, name, quantity, price, category FROM items"
            ).fetchall()

        return [Item(*row) for row in rows]

    def add_item(self, item: Item):
        with self.database.connect() as connection:
            connection.execute(
                """
                INSERT INTO items (name, quantity, price, category)
                VALUES (?, ?, ?, ?)
                """,
                (item.name, item.quantity, item.price, item.category)
            )

    def update_item(self, item: Item):
        with self.database.connect() as connection:
            connection.execute(
                """
                UPDATE items
                SET name = ?, quantity = ?, price = ?, category = ?
                WHERE id = ?
                """,
                (item.name, item.quantity, item.price, item.category, item.id)
            )

    def delete_item(self, item_id):
        with self.database.connect() as connection:
            connection.execute(
                "DELETE FROM items WHERE id = ?",
                (item_id,)
            )