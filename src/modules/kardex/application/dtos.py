from datetime import date
from typing import Optional
from pydantic import BaseModel


class CosechaCreate(BaseModel):
    fecha: date
    cosechero_id: int
    finca_id: int
    parcela_id: Optional[int] = None
    tipo_cosecha: str = "HOJA FRESCA"
    kg: float
    monto_bs: float = 0
    observacion: Optional[str] = None


class CosechaOut(CosechaCreate):
    id: int

    class Config:
        from_attributes = True


class MovimientoCreate(BaseModel):
    fecha: date
    detalle: str
    doc: Optional[str] = None
    lote_id: Optional[int] = None
    finca_id: Optional[int] = None
    entrada_kg: float = 0
    salida_kg: float = 0
    saldo_kg: float = 0
    observacion: Optional[str] = None


class MovimientoOut(MovimientoCreate):
    id: int

    class Config:
        from_attributes = True
