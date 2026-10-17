from .model import Category

class CategoryService:

    def __init__(self, repository, management_repository):
        self.repository = repository
        self.management_repository = management_repository

    def get_categories(self):
        return self.repository.get_categories()

    def add_category(self, name):
        name = name.strip()

        if not name:
            raise ValueError("Category name cannot be empty.")

        if self.repository.category_exists(name):
            raise ValueError("Category already exists.")

        self.repository.add_category(Category(name))

    def delete_category(self, name):
        name = name.strip()

        if not name:
            raise ValueError("Category name cannot be empty.")

        if name.lower() == "general":
            raise ValueError("The General category cannot be deleted.")

        if not self.repository.category_exists(name):
            raise ValueError("Category does not exist.")

        for item in self.management_repository.get_items():
            if item.category.lower() == name.lower():
                raise ValueError(
                    "Cannot delete a category that contains items."
                )

        self.repository.delete_category(name)

    def get_item_count(self, category_name):
        return sum(
            1 for item in self.management_repository.get_items()
            if item.category.lower() == category_name.lower()
        )