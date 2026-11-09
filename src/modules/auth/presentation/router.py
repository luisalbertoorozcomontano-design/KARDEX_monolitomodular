from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.modules.auth.application.dtos import UsuarioCreate, UsuarioLogin, UsuarioOut
from src.modules.auth.application.services import AuthService
from src.modules.auth.infrastructure.repository_impl import UsuarioRepositoryImpl
from src.modules.auth.domain.exceptions import UsuarioYaExiste, CredencialesInvalidas

router = APIRouter(prefix="/auth", tags=["auth"])


def get_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(UsuarioRepositoryImpl(db))


@router.post("/register", response_model=UsuarioOut)
def register(data: UsuarioCreate, service: AuthService = Depends(get_service)):
    try:
        return service.register(data)
    except UsuarioYaExiste as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
def login(data: UsuarioLogin, service: AuthService = Depends(get_service)):
    try:
        return service.login(data)
    except CredencialesInvalidas as e:
        raise HTTPException(status_code=401, detail=str(e))
