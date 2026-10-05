from dataclasses import dataclass

@dataclass
class ItemCalculation:
    name: str
    quantity: int
    price: float
    total_value: float

@dataclass
class InventorySummary:
    item_count: int
    total_quantity: int
    total_value: float