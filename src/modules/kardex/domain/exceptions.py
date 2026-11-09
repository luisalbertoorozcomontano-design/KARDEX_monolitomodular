class CosechaNoEncontrada(Exception):
    def __init__(self, cosecha_id: int):
        self.cosecha_id = cosecha_id
        super().__init__(f"Cosecha {cosecha_id} no encontrada")


class MovimientoNoEncontrado(Exception):
    def __init__(self, movimiento_id: int):
        self.movimiento_id = movimiento_id
        super().__init__(f"Movimiento {movimiento_id} no encontrado")
