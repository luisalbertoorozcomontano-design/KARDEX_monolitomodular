from sqlalchemy import Column, Integer, String, DECIMAL, Date, ForeignKey
from src.core.database import Base


class CosechaDB(Base):
    __tablename__ = "cosechas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    fecha = Column(Date, nullable=False)
    cosechero_id = Column(Integer, ForeignKey("cosecheros.id"), nullable=False)
    finca_id = Column(Integer, ForeignKey("fincas.id"), nullable=False)
    parcela_id = Column(Integer, ForeignKey("parcelas.id"), nullable=True)
    tipo_cosecha = Column(String(50), nullable=False, default="HOJA FRESCA")
    kg = Column(DECIMAL(12, 3), nullable=False)
    monto_bs = Column(DECIMAL(12, 2), nullable=False, default=0)
    observacion = Column(String(200), nullable=True)


class MovimientoDB(Base):
    __tablename__ = "kardex_movimientos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    fecha = Column(Date, nullable=False)
    detalle = Column(String(150), nullable=False)
    doc = Column(String(30), nullable=True)
    lote_id = Column(Integer, ForeignKey("lotes.id"), nullable=True)
    finca_id = Column(Integer, ForeignKey("fincas.id"), nullable=True)
    entrada_kg = Column(DECIMAL(12, 3), nullable=False, default=0)
    salida_kg = Column(DECIMAL(12, 3), nullable=False, default=0)
    saldo_kg = Column(DECIMAL(12, 3), nullable=False, default=0)
    observacion = Column(String(200), nullable=True)
