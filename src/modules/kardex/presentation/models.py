from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Cosecha:
    fecha: date
    cosechero_id: int
    finca_id: int
    kg: float
    parcela_id: Optional[int] = None
    tipo_cosecha: str = "HOJA FRESCA"
    monto_bs: float = 0
    observacion: Optional[str] = None
    id: Optional[int] = None


@dataclass
class Movimiento:
    fecha: date
    detalle: str
    entrada_kg: float = 0
    salida_kg: float = 0
    saldo_kg: float = 0
    doc: Optional[str] = None
    lote_id: Optional[int] = None
    finca_id: Optional[int] = None
    observacion: Optional[str] = None
    id: Optional[int] = None
