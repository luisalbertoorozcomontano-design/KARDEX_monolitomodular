class CosecheroNoEncontrado(Exception):
    def __init__(self, cosechero_id: int):
        self.cosechero_id = cosechero_id
        super().__init__(f"Cosechero {cosechero_id} no encontrado")
