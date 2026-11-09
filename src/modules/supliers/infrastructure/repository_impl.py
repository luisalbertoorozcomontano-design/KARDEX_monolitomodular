from typing import Optional, List
from sqlalchemy.orm import Session
from src.modules.supliers.domain.models import Cosechero
from src.modules.supliers.infrastructure.models_db import CosecheroDB


class CosecheroRepositoryImpl:
    def __init__(self, db: Session):
        self.db = db

    @staticmethod
    def _to_domain(row: CosecheroDB) -> Cosechero:
        return Cosechero(
            id=row.id,
            nombre=row.nombre,
            ci=row.ci,
            telefono=row.telefono,
            activo=row.activo,
        )

    def list_all(self) -> List[Cosechero]:
        rows = self.db.query(CosecheroDB).all()
        return [self._to_domain(row) for row in rows]

    def get_by_id(self, cosechero_id: int) -> Optional[Cosechero]:
        row = self.db.query(CosecheroDB).get(cosechero_id)
        return self._to_domain(row) if row else None

    def add(self, cosechero: Cosechero) -> Cosechero:
        row = CosecheroDB(nombre=cosechero.nombre, ci=cosechero.ci, telefono=cosechero.telefono)
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return self._to_domain(row)

    def update(self, cosechero: Cosechero) -> Cosechero:
        row = self.db.query(CosecheroDB).get(cosechero.id)
        row.nombre = cosechero.nombre
        row.ci = cosechero.ci
        row.telefono = cosechero.telefono
        row.activo = cosechero.activo
        self.db.commit()
        self.db.refresh(row)
        return self._to_domain(row)
