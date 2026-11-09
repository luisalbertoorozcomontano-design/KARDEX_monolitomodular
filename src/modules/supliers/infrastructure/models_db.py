from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, func
from src.core.database import Base


class CosecheroDB(Base):
    __tablename__ = "cosecheros"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    ci = Column(String(20), nullable=True)
    telefono = Column(String(20), nullable=True)
    activo = Column(Boolean, nullable=False, default=True)
    creado_en = Column(TIMESTAMP, server_default=func.now())
