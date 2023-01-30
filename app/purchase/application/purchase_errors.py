class EmptyDetailError(Exception):
    def __init__(self):
        self.message = "Purchase detail must contain at least one item"
        super().__init__(self.message)


class NotEnoughStockError(Exception):
    def __init__(self, item_name: str):
        self.message = f"Not enough stock for {item_name}"
        super().__init__(self.message)


class NoCustomerError(Exception):
    def __init__(self):
        self.message = "The purchase must have a customer id"
        super().__init__(self.message)


class NotEnoughBudgetError(Exception):
    def __init__(self):
        self.message = f"Not enough budget for the purchase"
        super().__init__(self.message)
