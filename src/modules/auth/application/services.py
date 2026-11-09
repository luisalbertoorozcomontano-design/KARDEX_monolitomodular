from src.modules.auth.domain.models import Usuario
from src.modules.auth.domain.repositories import UsuarioRepository
from src.modules.auth.domain.exceptions import UsuarioYaExiste, CredencialesInvalidas
from src.modules.auth.application.dtos import UsuarioCreate, UsuarioLogin
from src.modules.auth.infrastructure.external_adapters import PasswordHasher


class AuthService:
    def __init__(self, repository: UsuarioRepository):
        self.repository = repository

    def list_all(self):
        return self.repository.list_all()

    def register(self, data: UsuarioCreate) -> Usuario:
        if self.repository.exists_username(data.username):
            raise UsuarioYaExiste(data.username)
        usuario = Usuario(
            username=data.username,
            password_hash=PasswordHasher.hash(data.password),
            nombre_completo=data.nombre_completo,
            rol=data.rol,
        )
        return self.repository.add(usuario)

    def login(self, data: UsuarioLogin) -> dict:
        usuario = self.repository.get_by_username(data.username)
        if not usuario or not PasswordHasher.verify(data.password, usuario.password_hash):
            raise CredencialesInvalidas()
        return {"msg": "Login exitoso", "usuario": usuario.username, "rol": usuario.rol}
