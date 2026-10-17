from .model import StackEntry

class StackService:

    def __init__(self, repository):
        self.repository = repository

    def push(self, item):
        if item is None or item.id is None:
            raise ValueError(
                "Please select a valid inventory item."
            )

        entry = StackEntry(
            item_id=item.id,
            name=item.name,
            quantity=item.quantity,
            price=item.price,
            category=item.category
        )

        self.repository.push(entry)

        return entry

    def pop(self):
        return self.repository.pop()

    def peek(self):
        return self.repository.peek()

    def get_stack(self):
        return self.repository.get_stack()

    def size(self):
        return self.repository.size()