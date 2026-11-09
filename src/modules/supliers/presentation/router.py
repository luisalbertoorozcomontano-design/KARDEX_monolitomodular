from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.modules.supliers.application.dtos import CosecheroCreate, CosecheroOut
from src.modules.supliers.application.services import CosecheroService
from src.modules.supliers.infrastructure.repository_impl import CosecheroRepositoryImpl
from src.modules.supliers.domain.exceptions import CosecheroNoEncontrado

router = APIRouter(prefix="/cosecheros", tags=["cosecheros"])


def get_service(db: Session = Depends(get_db)) -> CosecheroService:
    return CosecheroService(CosecheroRepositoryImpl(db))


@router.get("", response_model=list[CosecheroOut])
def listar(service: CosecheroService = Depends(get_service)):
    return service.list_all()


@router.get("/{cosechero_id}", response_model=CosecheroOut)
def obtener(cosechero_id: int, service: CosecheroService = Depends(get_service)):
    try:
        return service.get_by_id(cosechero_id)
    except CosecheroNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("", response_model=CosecheroOut)
def crear(data: CosecheroCreate, service: CosecheroService = Depends(get_service)):
    return service.create(data)


@router.put("/{cosechero_id}", response_model=CosecheroOut)
def actualizar(cosechero_id: int, data: CosecheroCreate, service: CosecheroService = Depends(get_service)):
    try:
        return service.update(cosechero_id, data)
    except CosecheroNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{cosechero_id}")
def eliminar(cosechero_id: int, service: CosecheroService = Depends(get_service)):
    try:
        service.delete(cosechero_id)
    except CosecheroNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"msg": "Cosechero desactivado"}
