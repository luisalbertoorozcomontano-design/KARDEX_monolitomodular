from sqlalchemy import Column, Integer, String, Boolean, DECIMAL, Date, TIMESTAMP, ForeignKey, func
from src.core.database import Base


class FincaDB(Base):
    __tablename__ = "fincas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    numero = Column(Integer, unique=True, nullable=False)
    nombre = Column(String(100), nullable=True)
    ubicacion = Column(String(150), nullable=True)
    activo = Column(Boolean, nullable=False, default=True)


class ParcelaDB(Base):
    __tablename__ = "parcelas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    finca_id = Column(Integer, ForeignKey("fincas.id"), nullable=False)
    numero = Column(Integer, nullable=False)
    superficie_ha = Column(DECIMAL(10, 2), nullable=True)
    activo = Column(Boolean, nullable=False, default=True)


class LoteDB(Base):
    __tablename__ = "lotes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    codigo = Column(String(30), unique=True, nullable=False)
    finca_id = Column(Integer, ForeignKey("fincas.id"), nullable=True)
    fecha_ingreso = Column(Date, nullable=False)
    detalle = Column(String(150), nullable=True)
    creado_en = Column(TIMESTAMP, server_default=func.now())
