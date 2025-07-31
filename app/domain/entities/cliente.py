import uuid
from app.domain.exceptions import InvalidEmail, InvalidCPF, InvalidPhone


class ClienteEntity:

    def __init__(
        self,
        uid: str,
        nome: str,
        telefone: str = None,
        email: str = None,
        cpf: str = None,
    ):
        self.__validate_email(email)
        self.__validate_cpf(cpf)
        self.__validate_phone(telefone)

        self.id = uid
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.cpf = cpf

    @staticmethod
    def __validate_email(email: str):
        if email and "@" not in email:
            raise InvalidEmail

    @staticmethod
    def __validate_cpf(cpf: str):
        if cpf and len(cpf.replace(".", "").replace("-", "")) != 11:
            raise InvalidCPF

    @staticmethod
    def __validate_phone(telefone: str):
        if (
            telefone
            and len(
                telefone.replace("(", "")
                .replace(")", "")
                .replace("-", "")
                .replace(" ", "")
            )
            < 10
        ):
            raise InvalidPhone


class ClienteEntityFactory:

    @staticmethod
    def create(
        id: str | None,
        nome: str,
        telefone: str = None,
        email: str = None,
        cpf: str = None,
    ) -> ClienteEntity:
        if id is None:
            id = uuid.uuid4().__str__()
        return ClienteEntity(id, nome, telefone, email, cpf)
