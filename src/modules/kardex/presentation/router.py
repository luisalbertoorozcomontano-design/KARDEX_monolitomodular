from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.modules.kardex.application.dtos import CosechaCreate, CosechaOut, MovimientoCreate, MovimientoOut
from src.modules.kardex.application.services import CosechaService, MovimientoService
from src.modules.kardex.infrastructure.repository_impl import CosechaRepositoryImpl, MovimientoRepositoryImpl
from src.modules.kardex.domain.exceptions import CosechaNoEncontrada

router = APIRouter(prefix="/kardex", tags=["kardex"])


def get_cosecha_service(db: Session = Depends(get_db)) -> CosechaService:
    return CosechaService(CosechaRepositoryImpl(db))


def get_movimiento_service(db: Session = Depends(get_db)) -> MovimientoService:
    return MovimientoService(MovimientoRepositoryImpl(db))


@router.get("/cosechas", response_model=list[CosechaOut])
def listar_cosechas(service: CosechaService = Depends(get_cosecha_service)):
    return service.list_all()


@router.post("/cosechas", response_model=CosechaOut)
def crear_cosecha(data: CosechaCreate, service: CosechaService = Depends(get_cosecha_service)):
    return service.create(data)


@router.get("/cosechas/total-kg")
def total_kg_mes(anio: int, mes: int, service: CosechaService = Depends(get_cosecha_service)):
    total = service.total_kg_by_month(anio, mes)
    return {"anio": anio, "mes": mes, "total_kg": total}


@router.get("/movimientos", response_model=list[MovimientoOut])
def listar_movimientos(service: MovimientoService = Depends(get_movimiento_service)):
    return service.list_all()


@router.post("/movimientos", response_model=MovimientoOut)
def crear_movimiento(data: MovimientoCreate, service: MovimientoService = Depends(get_movimiento_service)):
    return service.create(data)
