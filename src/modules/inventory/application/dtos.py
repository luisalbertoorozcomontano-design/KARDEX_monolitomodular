from datetime import date
from typing import Optional
from pydantic import BaseModel


class FincaCreate(BaseModel):
    numero: int
    nombre: Optional[str] = None
    ubicacion: Optional[str] = None


class FincaOut(FincaCreate):
    id: int
    activo: bool

    class Config:
        from_attributes = True


class ParcelaCreate(BaseModel):
    finca_id: int
    numero: int
    superficie_ha: Optional[float] = None


class ParcelaOut(ParcelaCreate):
    id: int
    activo: bool

    class Config:
        from_attributes = True


class LoteCreate(BaseModel):
    codigo: str
    finca_id: Optional[int] = None
    fecha_ingreso: date
    detalle: Optional[str] = None


class LoteOut(LoteCreate):
    id: int

    class Config:
        from_attributes = True
