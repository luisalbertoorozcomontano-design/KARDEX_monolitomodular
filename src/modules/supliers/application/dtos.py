from typing import Optional
from pydantic import BaseModel


class CosecheroCreate(BaseModel):
    nombre: str
    ci: Optional[str] = None
    telefono: Optional[str] = None


class CosecheroOut(CosecheroCreate):
    id: int
    activo: bool

    class Config:
        from_attributes = True
