class DomainError(Exception):
    """Base class for all domain-level exceptions."""


class EntityNotFound(DomainError):
    def __init__(self, entity: str = "Entity"):
        super().__init__(f"{entity} not found")


class EntityAlreadyExists(DomainError):
    def __init__(self, entity: str = "Entity"):
        super().__init__(f"{entity} already exists")


class InvalidDataError(DomainError):
    def __init__(self, message: str = "Invalid data"):
        super().__init__(message)

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


class InvalidName(Exception):
    def __init__(self):
        super().__init__("O nome informado é inválido. Ele deve ter pelo menos 3 caracteres.")


class InvalidPassword(Exception):
    def __init__(self):
        super().__init__("A senha informada é inválida. Ela deve ter pelo menos 8 caracteres.")

class ClienteNotFound(DomainError):
    """Exceção lançada quando um cliente não é encontrado"""
    pass

class ServicoNotFound(DomainError):
    """Exceção lançada quando um serviço não é encontrado"""
    pass

class VehicleNotFound(DomainError):
    """Exceção lançada quando um veículo não é encontrado"""
    pass