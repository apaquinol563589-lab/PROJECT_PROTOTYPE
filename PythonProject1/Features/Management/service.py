from .model import Item

class ManagementService:

    def __init__(self, repository, category_repository):
        self.repository = repository
        self.categories = category_repository

    def get_items(self):
        return self.repository.get_items()

    def get_categories(self):
        return self.categories.get_categories()

    def make_item(self, item_id, name, quantity, price, category):
        name = name.strip()
        category = category.strip()

        if not name:
            raise ValueError("Category name cannot be empty.")

        try:
            quantity = int(quantity)
            price = float(price)
        except ValueError:
            raise ValueError(
                "Quantity must be a number and price must be numeric."
            )

        if quantity < 0 or price < 0:
            raise ValueError("Quantity and price cannot be negative.")

        actual_category = self.categories.get_category(category)

        if not actual_category:
            raise ValueError("Invalid category.")

        return Item(
            item_id,
            name,
            quantity,
            price,
            actual_category.name
        )

    def add_item(self, name, quantity, price, category):
        item = self.make_item(
            None, name, quantity, price, category
        )
        self.repository.add_item(item)

    def update_item(self, item_id, name, quantity, price, category):
        item = self.make_item(
            item_id, name, quantity, price, category
        )
        self.repository.update_item(item)

    def delete_item(self, item_id):
        self.repository.delete_item(item_id)