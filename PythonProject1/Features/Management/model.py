from dataclasses import dataclass

@dataclass
class Item:
    id: int | None
    name: str
    quantity: int
    price: float
    category: str = "General"