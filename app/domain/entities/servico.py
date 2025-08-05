import uuid
from app.domain.exceptions import PriceIsLessThanOrEqualToZero, InvalidDescription


class ServicoEntity:

    def __init__(self, uid: str, descricao: str, preco: float):
        self.__validate_preco(preco)
        self.__validate_descricao(descricao)

        self.id = uid
        self.descricao = descricao
        self.preco = preco

    @staticmethod
    def __validate_preco(preco: float):
        if preco <= 0:
            raise PriceIsLessThanOrEqualToZero

    @staticmethod
    def __validate_descricao(descricao: str):
        if not descricao or len(descricao.strip()) == 0:
            raise InvalidDescription


class ServicoEntityFactory:

    @staticmethod
    def create(id: str | None, descricao: str, preco: float) -> ServicoEntity:
        if id is None:
            id = uuid.uuid4().__str__()
        return ServicoEntity(id, descricao, float(preco))
