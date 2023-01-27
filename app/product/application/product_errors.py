class ProductFoundError(Exception):
    def __init__(self):
        self.message = "Product already exists"
        super().__init__(self.message)


class ProductNotFoundError(Exception):
    def __init__(self, id: str | None = None):
        if not id:
            self.message = "Product not found"
        else:
            self.message = f"Product ID '{id}' not found"

        super().__init__(self.message)

