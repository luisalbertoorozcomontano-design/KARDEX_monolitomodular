from dataclasses import dataclass
from typing import Optional


@dataclass
class Usuario:
    username: str
    password_hash: str
    nombre_completo: str
    rol: str = "operador"
    id: Optional[int] = None
    activo: bool = True
