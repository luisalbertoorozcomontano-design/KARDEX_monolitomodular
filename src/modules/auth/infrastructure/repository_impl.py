from typing import Optional, List
from sqlalchemy.orm import Session
from src.modules.auth.domain.models import Usuario
from src.modules.auth.infrastructure.models_db import UsuarioDB


class UsuarioRepositoryImpl:
    def __init__(self, db: Session):
        self.db = db

    @staticmethod
    def _to_domain(row: UsuarioDB) -> Usuario:
        return Usuario(
            id=row.id,
            username=row.username,
            password_hash=row.password_hash,
            nombre_completo=row.nombre_completo,
            rol=row.rol,
            activo=row.activo,
        )

    def list_all(self) -> List[Usuario]:
        rows = self.db.query(UsuarioDB).all()
        return [self._to_domain(row) for row in rows]

    def get_by_id(self, usuario_id: int) -> Optional[Usuario]:
        row = self.db.query(UsuarioDB).get(usuario_id)
        return self._to_domain(row) if row else None

    def get_by_username(self, username: str) -> Optional[Usuario]:
        row = self.db.query(UsuarioDB).filter(UsuarioDB.username == username).first()
        return self._to_domain(row) if row else None

    def exists_username(self, username: str) -> bool:
        return self.db.query(UsuarioDB).filter(UsuarioDB.username == username).first() is not None

    def add(self, usuario: Usuario) -> Usuario:
        row = UsuarioDB(
            username=usuario.username,
            password_hash=usuario.password_hash,
            nombre_completo=usuario.nombre_completo,
            rol=usuario.rol,
        )
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return self._to_domain(row)
