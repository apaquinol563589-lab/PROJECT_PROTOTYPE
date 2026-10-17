from dataclasses import dataclass

@dataclass
class Category:
    name: str

    def to_dict(self):
        return {"name": self.name}

    @staticmethod
    def from_dict(data):
        if isinstance(data, str):
            return Category(data)

        return Category(str(data.get("name", "General")))