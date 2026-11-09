from typing import Optional, List
from sqlalchemy.orm import Session
from src.modules.inventory.domain.models import Finca, Parcela, Lote
from src.modules.inventory.infrastructure.models_db import FincaDB, ParcelaDB, LoteDB


class FincaRepositoryImpl:
    def __init__(self, db: Session):
        self.db = db

    @staticmethod
    def _to_domain(row: FincaDB) -> Finca:
        return Finca(id=row.id, numero=row.numero, nombre=row.nombre, ubicacion=row.ubicacion, activo=row.activo)

    def list_all(self) -> List[Finca]:
        rows = self.db.query(FincaDB).all()
        return [self._to_domain(row) for row in rows]

    def get_by_id(self, finca_id: int) -> Optional[Finca]:
        row = self.db.query(FincaDB).get(finca_id)
        return self._to_domain(row) if row else None

    def add(self, finca: Finca) -> Finca:
        row = FincaDB(numero=finca.numero, nombre=finca.nombre, ubicacion=finca.ubicacion)
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return self._to_domain(row)


class ParcelaRepositoryImpl:
    def __init__(self, db: Session):
        self.db = db

    @staticmethod
    def _to_domain(row: ParcelaDB) -> Parcela:
        return Parcela(id=row.id, finca_id=row.finca_id, numero=row.numero, superficie_ha=float(row.superficie_ha) if row.superficie_ha else None, activo=row.activo)

    def list_all(self) -> List[Parcela]:
        rows = self.db.query(ParcelaDB).all()
        return [self._to_domain(row) for row in rows]

    def get_by_id(self, parcela_id: int) -> Optional[Parcela]:
        row = self.db.query(ParcelaDB).get(parcela_id)
        return self._to_domain(row) if row else None

    def add(self, parcela: Parcela) -> Parcela:
        row = ParcelaDB(finca_id=parcela.finca_id, numero=parcela.numero, superficie_ha=parcela.superficie_ha)
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return self._to_domain(row)


class LoteRepositoryImpl:
    def __init__(self, db: Session):
        self.db = db

    @staticmethod
    def _to_domain(row: LoteDB) -> Lote:
        return Lote(id=row.id, codigo=row.codigo, finca_id=row.finca_id, fecha_ingreso=row.fecha_ingreso, detalle=row.detalle)

    def list_all(self) -> List[Lote]:
        rows = self.db.query(LoteDB).all()
        return [self._to_domain(row) for row in rows]

    def get_by_id(self, lote_id: int) -> Optional[Lote]:
        row = self.db.query(LoteDB).get(lote_id)
        return self._to_domain(row) if row else None

    def exists_codigo(self, codigo: str) -> bool:
        return self.db.query(LoteDB).filter(LoteDB.codigo == codigo).first() is not None

    def add(self, lote: Lote) -> Lote:
        row = LoteDB(codigo=lote.codigo, finca_id=lote.finca_id, fecha_ingreso=lote.fecha_ingreso, detalle=lote.detalle)
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return self._to_domain(row)
