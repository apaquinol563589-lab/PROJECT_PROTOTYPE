class CalculateService:

    def __init__(self, repository):
        self.repository = repository

    def get_item_calculations(self):
        return self.repository.get_item_calculations()

    def get_summary(self):
        return self.repository.get_summary()

    def get_item_total(self, item_name):
        if not item_name or not item_name.strip():
            raise ValueError("Category name cannot be empty.")

        return self.repository.get_item_total(item_name.strip())