from sqlalchemy import Column, Integer, String, DECIMAL, DateTime
from sqlalchemy.sql import func
from app.infrastructure.database import Base


class ServicoModel(Base):
    __tablename__ = "servicos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(255), nullable=False)
    preco = Column(DECIMAL(precision=10, scale=2), nullable=False)
    atualizado_em = Column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "descricao": self.descricao,
            "preco": float(self.preco) if self.preco else 0.0,
            "atualizado_em": (
                self.atualizado_em.isoformat() if self.atualizado_em else None
            ),
        }
