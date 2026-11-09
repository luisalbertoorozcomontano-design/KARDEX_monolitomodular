from typing import Optional
from pydantic import BaseModel


class UsuarioCreate(BaseModel):
    username: str
    password: str
    nombre_completo: str
    rol: str = "operador"


class UsuarioLogin(BaseModel):
    username: str
    password: str


class UsuarioOut(BaseModel):
    id: int
    username: str
    nombre_completo: str
    rol: str
    activo: bool

    class Config:
        from_attributes = True
