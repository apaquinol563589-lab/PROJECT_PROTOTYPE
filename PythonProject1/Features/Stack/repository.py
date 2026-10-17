from .model import StackEntry

class StackRepository:

    def __init__(self):
        self.stack = []

    def push(self, entry: StackEntry):
        self.stack.append(entry)

    def pop(self):
        if not self.stack:
            raise ValueError("The stack is empty.")

        return self.stack.pop()

    def peek(self):
        if not self.stack:
            raise ValueError("The stack is empty.")

        return self.stack[-1]

    def get_stack(self):
        # Display the top item first
        return list(reversed(self.stack))

    def size(self):
        return len(self.stack)
