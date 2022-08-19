
class MockDb():
    def __init__(self, items: dict) -> None:
        self.items = items

    def get_items(self):
        return self.items

    def set_items(self, items:dict):
        self.items = items