class UsuarioYaExiste(Exception):
    def __init__(self, username: str):
        self.username = username
        super().__init__(f"El usuario {username} ya existe")


class CredencialesInvalidas(Exception):
    def __init__(self):
        super().__init__("Usuario o contraseña incorrectos")
