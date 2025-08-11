from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.infrastructure.database import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True)
    nome = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    funcao = Column(String(100), nullable=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    atualizado_em = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "funcao": self.funcao,
            "criado_em": self.criado_em.isoformat() if self.criado_em else None,
            "atualizado_em": self.atualizado_em.isoformat() if self.atualizado_em else None,
        }
