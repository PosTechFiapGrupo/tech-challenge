class InvalidDescription(Exception):
    def __init__(self):
        super().__init__("The description must have less than 50 characters")


class InvalidPrice(Exception):
    def __init__(self):
        super().__init__("The price is not a valid number")


class PriceIsLessThanOrEqualToZero(Exception):
    def __init__(self):
        super().__init__("The price is less than or equal to zero")


class StockIsLessThanOrEqualToZero(Exception):
    def __init__(self):
        super().__init__("The stock is less than or equal to zero")


class InvalidEmail(Exception):
    def __init__(self):
        super().__init__("The email format is invalid")


class InvalidCPF(Exception):
    def __init__(self):
        super().__init__("The CPF must have 11 digits")


class InvalidPhone(Exception):
    def __init__(self):
        super().__init__("The phone number must have at least 10 digits")
