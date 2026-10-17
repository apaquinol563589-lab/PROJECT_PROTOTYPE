from dataclasses import dataclass

@dataclass
class StackEntry:
    item_id: int
    name: str
    quantity: int
    price: float
    category: str
