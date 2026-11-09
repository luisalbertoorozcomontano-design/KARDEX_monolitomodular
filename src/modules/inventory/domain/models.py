from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Finca:
    numero: int
    nombre: Optional[str] = None
    ubicacion: Optional[str] = None
    id: Optional[int] = None
    activo: bool = True


@dataclass
class Parcela:
    finca_id: int
    numero: int
    superficie_ha: Optional[float] = None
    id: Optional[int] = None
    activo: bool = True


@dataclass
class Lote:
    codigo: str
    fecha_ingreso: date
    finca_id: Optional[int] = None
    detalle: Optional[str] = None
    id: Optional[int] = None
