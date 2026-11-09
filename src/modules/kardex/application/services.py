from src.modules.kardex.domain.models import Cosecha, Movimiento
from src.modules.kardex.domain.repositories import CosechaRepository, MovimientoRepository
from src.modules.kardex.domain.exceptions import CosechaNoEncontrada
from src.modules.kardex.application.dtos import CosechaCreate, MovimientoCreate


class CosechaService:
    def __init__(self, repository: CosechaRepository):
        self.repository = repository

    def list_all(self):
        return self.repository.list_all()

    def get_by_id(self, cosecha_id: int) -> Cosecha:
        cosecha = self.repository.get_by_id(cosecha_id)
        if not cosecha:
            raise CosechaNoEncontrada(cosecha_id)
        return cosecha

    def create(self, data: CosechaCreate) -> Cosecha:
        cosecha = Cosecha(
            fecha=data.fecha,
            cosechero_id=data.cosechero_id,
            finca_id=data.finca_id,
            parcela_id=data.parcela_id,
            tipo_cosecha=data.tipo_cosecha,
            kg=data.kg,
            monto_bs=data.monto_bs,
            observacion=data.observacion,
        )
        return self.repository.add(cosecha)

    def total_kg_by_month(self, anio: int, mes: int) -> float:
        return self.repository.total_kg_by_month(anio, mes)


class MovimientoService:
    def __init__(self, repository: MovimientoRepository):
        self.repository = repository

    def list_all(self):
        return self.repository.list_all()

    def create(self, data: MovimientoCreate) -> Movimiento:
        ultimo = self.repository.get_last()
        saldo_anterior = float(ultimo.saldo_kg) if ultimo else 0
        saldo = data.saldo_kg
        if saldo == 0:
            saldo = saldo_anterior + data.entrada_kg - data.salida_kg
        movimiento = Movimiento(
            fecha=data.fecha,
            detalle=data.detalle,
            doc=data.doc,
            lote_id=data.lote_id,
            finca_id=data.finca_id,
            entrada_kg=data.entrada_kg,
            salida_kg=data.salida_kg,
            saldo_kg=saldo,
            observacion=data.observacion,
        )
        return self.repository.add(movimiento)
