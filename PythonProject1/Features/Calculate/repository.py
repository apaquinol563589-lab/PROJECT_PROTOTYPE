from .model import ItemCalculation, InventorySummary

class CalculateRepository:

    def __init__(self, management_repository):
        self.management_repository = management_repository

    def get_item_calculations(self):
        items = self.management_repository.get_items()

        calculations = []

        for item in items:
            total_value = item.quantity * item.price

            calculation = ItemCalculation(
                name=item.name,
                quantity=item.quantity,
                price=item.price,
                total_value=total_value
            )

            calculations.append(calculation)

        return calculations

    def get_summary(self):
        calculations = self.get_item_calculations()

        item_count = len(calculations)

        total_quantity = sum(
            item.quantity for item in calculations
        )

        total_value = sum(
            item.total_value for item in calculations
        )

        return InventorySummary(
            item_count=item_count,
            total_quantity=total_quantity,
            total_value=total_value
        )

    def get_item_total(self, item_name):
        calculations = self.get_item_calculations()

        for item in calculations:
            if item.name.lower() == item_name.lower():
                return item.total_value

        return None