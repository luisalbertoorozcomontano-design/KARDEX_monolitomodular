from src.modules.supliers.domain.models import Cosechero
from src.modules.supliers.domain.repositories import CosecheroRepository
from src.modules.supliers.domain.exceptions import CosecheroNoEncontrado
from src.modules.supliers.application.dtos import CosecheroCreate


class CosecheroService:
    def __init__(self, repository: CosecheroRepository):
        self.repository = repository

    def list_all(self):
        return self.repository.list_all()

    def get_by_id(self, cosechero_id: int) -> Cosechero:
        cosechero = self.repository.get_by_id(cosechero_id)
        if not cosechero:
            raise CosecheroNoEncontrado(cosechero_id)
        return cosechero

    def create(self, data: CosecheroCreate) -> Cosechero:
        cosechero = Cosechero(nombre=data.nombre, ci=data.ci, telefono=data.telefono)
        return self.repository.add(cosechero)

    def update(self, cosechero_id: int, data: CosecheroCreate) -> Cosechero:
        cosechero = self.get_by_id(cosechero_id)
        cosechero.nombre = data.nombre
        cosechero.ci = data.ci
        cosechero.telefono = data.telefono
        return self.repository.update(cosechero)

    def delete(self, cosechero_id: int) -> None:
        cosechero = self.get_by_id(cosechero_id)
        cosechero.activo = False
        self.repository.update(cosechero)
