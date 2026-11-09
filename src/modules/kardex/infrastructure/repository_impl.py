from typing import Optional, List
from sqlalchemy import func, extract
from sqlalchemy.orm import Session
from src.modules.kardex.domain.models import Cosecha, Movimiento
from src.modules.kardex.infrastructure.models_db import CosechaDB, MovimientoDB


class CosechaRepositoryImpl:
    def __init__(self, db: Session):
        self.db = db

    @staticmethod
    def _to_domain(row: CosechaDB) -> Cosecha:
        return Cosecha(
            id=row.id,
            fecha=row.fecha,
            cosechero_id=row.cosechero_id,
            finca_id=row.finca_id,
            parcela_id=row.parcela_id,
            tipo_cosecha=row.tipo_cosecha,
            kg=float(row.kg),
            monto_bs=float(row.monto_bs),
            observacion=row.observacion,
        )

    def list_all(self) -> List[Cosecha]:
        rows = self.db.query(CosechaDB).order_by(CosechaDB.fecha).all()
        return [self._to_domain(row) for row in rows]

    def get_by_id(self, cosecha_id: int) -> Optional[Cosecha]:
        row = self.db.query(CosechaDB).get(cosecha_id)
        return self._to_domain(row) if row else None

    def add(self, cosecha: Cosecha) -> Cosecha:
        row = CosechaDB(
            fecha=cosecha.fecha,
            cosechero_id=cosecha.cosechero_id,
            finca_id=cosecha.finca_id,
            parcela_id=cosecha.parcela_id,
            tipo_cosecha=cosecha.tipo_cosecha,
            kg=cosecha.kg,
            monto_bs=cosecha.monto_bs,
            observacion=cosecha.observacion,
        )
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return self._to_domain(row)

    def total_kg_by_month(self, anio: int, mes: int) -> float:
        total = (
            self.db.query(func.sum(CosechaDB.kg))
            .filter(
                extract("year", CosechaDB.fecha) == anio,
                extract("month", CosechaDB.fecha) == mes,
            )
            .scalar()
        )
        return float(total or 0)


class MovimientoRepositoryImpl:
    def __init__(self, db: Session):
        self.db = db

    @staticmethod
    def _to_domain(row: MovimientoDB) -> Movimiento:
        return Movimiento(
            id=row.id,
            fecha=row.fecha,
            detalle=row.detalle,
            doc=row.doc,
            lote_id=row.lote_id,
            finca_id=row.finca_id,
            entrada_kg=float(row.entrada_kg),
            salida_kg=float(row.salida_kg),
            saldo_kg=float(row.saldo_kg),
            observacion=row.observacion,
        )

    def list_all(self) -> List[Movimiento]:
        rows = self.db.query(MovimientoDB).order_by(MovimientoDB.fecha).all()
        return [self._to_domain(row) for row in rows]

    def get_by_id(self, movimiento_id: int) -> Optional[Movimiento]:
        row = self.db.query(MovimientoDB).get(movimiento_id)
        return self._to_domain(row) if row else None

    def get_last(self) -> Optional[Movimiento]:
        row = self.db.query(MovimientoDB).order_by(MovimientoDB.id.desc()).first()
        return self._to_domain(row) if row else None

    def add(self, movimiento: Movimiento) -> Movimiento:
        row = MovimientoDB(
            fecha=movimiento.fecha,
            detalle=movimiento.detalle,
            doc=movimiento.doc,
            lote_id=movimiento.lote_id,
            finca_id=movimiento.finca_id,
            entrada_kg=movimiento.entrada_kg,
            salida_kg=movimiento.salida_kg,
            saldo_kg=movimiento.saldo_kg,
            observacion=movimiento.observacion,
        )
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return self._to_domain(row)
