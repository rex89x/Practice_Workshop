class Item:
    def __init__(self, title, price, description):
        self.title = title
        self.price = price
        self.description = description

    def __repr__(self):
        return f"Item(title={self.title}, price={self.price}, description={self.description})"