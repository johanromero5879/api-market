class ProductFoundError(Exception):
    def __init__(self):
        self.message = "Product already exists"
        super().__init__(self.message)


class ProductNotFoundError(Exception):
    def __init__(self):
        self.message = "Product not found"
        super().__init__(self.message)

