from app.domain.exceptions import InvalidPrice, PriceIsLessThanOrEqualToZero


class ServicoValidator:

    @staticmethod
    def validate_preco(preco: float) -> float:
        try:
            preco_float = float(preco)
            if preco_float <= 0:
                raise PriceIsLessThanOrEqualToZero
            return preco_float
        except ValueError:
            raise InvalidPrice

    @staticmethod
    def validate_descricao(descricao: str) -> None:
        if not descricao or len(descricao.strip()) == 0:
            raise ValueError("Descrição é obrigatória")
        if len(descricao) > 255:
            raise ValueError("Descrição deve ter no máximo 255 caracteres")
