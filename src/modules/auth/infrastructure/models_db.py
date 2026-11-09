from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, func
from src.core.database import Base


class UsuarioDB(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    nombre_completo = Column(String(100), nullable=False)
    rol = Column(String(32), nullable=False, default="operador")
    activo = Column(Boolean, nullable=False, default=True)
    creado_en = Column(TIMESTAMP, server_default=func.now())
