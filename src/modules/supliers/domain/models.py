from dataclasses import dataclass
from typing import Optional


@dataclass
class Cosechero:
    nombre: str
    ci: Optional[str] = None
    telefono: Optional[str] = None
    id: Optional[int] = None
    activo: bool = True
