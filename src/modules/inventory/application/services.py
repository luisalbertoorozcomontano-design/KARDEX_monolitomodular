from src.modules.inventory.domain.models import Finca, Parcela, Lote
from src.modules.inventory.domain.repositories import FincaRepository, ParcelaRepository, LoteRepository
from src.modules.inventory.domain.exceptions import FincaNoEncontrada, LoteDuplicado
from src.modules.inventory.application.dtos import FincaCreate, ParcelaCreate, LoteCreate


class FincaService:
    def __init__(self, repository: FincaRepository):
        self.repository = repository

    def list_all(self):
        return self.repository.list_all()

    def get_by_id(self, finca_id: int) -> Finca:
        finca = self.repository.get_by_id(finca_id)
        if not finca:
            raise FincaNoEncontrada(finca_id)
        return finca

    def create(self, data: FincaCreate) -> Finca:
        finca = Finca(numero=data.numero, nombre=data.nombre, ubicacion=data.ubicacion)
        return self.repository.add(finca)


class ParcelaService:
    def __init__(self, parcela_repo: ParcelaRepository, finca_repo: FincaRepository):
        self.parcela_repo = parcela_repo
        self.finca_repo = finca_repo

    def list_all(self):
        return self.parcela_repo.list_all()

    def create(self, data: ParcelaCreate) -> Parcela:
        finca = self.finca_repo.get_by_id(data.finca_id)
        if not finca:
            raise FincaNoEncontrada(data.finca_id)
        parcela = Parcela(
            finca_id=data.finca_id,
            numero=data.numero,
            superficie_ha=data.superficie_ha,
        )
        return self.parcela_repo.add(parcela)


class LoteService:
    def __init__(self, repository: LoteRepository):
        self.repository = repository

    def list_all(self):
        return self.repository.list_all()

    def create(self, data: LoteCreate) -> Lote:
        if self.repository.exists_codigo(data.codigo):
            raise LoteDuplicado(data.codigo)
        lote = Lote(
            codigo=data.codigo,
            finca_id=data.finca_id,
            fecha_ingreso=data.fecha_ingreso,
            detalle=data.detalle,
        )
        return self.repository.add(lote)
