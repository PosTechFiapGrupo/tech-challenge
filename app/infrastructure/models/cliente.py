from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from app.infrastructure.database import Base


class ClienteModel(Base):
    __tablename__ = "clientes"

    id = Column(String(36), primary_key=True)
    nome = Column(String(100), nullable=False)
    telefone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    cpf = Column(String(14), nullable=True)
    criado_em = Column(DateTime, nullable=False, server_default=func.now())
    atualizado_em = Column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nome": self.nome,
            "telefone": self.telefone,
            "email": self.email,
            "cpf": self.cpf,
            "criado_em": self.criado_em.isoformat() if self.criado_em else None,
            "atualizado_em": (
                self.atualizado_em.isoformat() if self.atualizado_em else None
            ),
        }
