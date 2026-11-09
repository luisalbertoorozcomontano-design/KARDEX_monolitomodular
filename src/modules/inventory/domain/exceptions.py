class FincaNoEncontrada(Exception):
    def __init__(self, finca_id: int):
        self.finca_id = finca_id
        super().__init__(f"Finca {finca_id} no encontrada")


class ParcelaNoEncontrada(Exception):
    def __init__(self, parcela_id: int):
        self.parcela_id = parcela_id
        super().__init__(f"Parcela {parcela_id} no encontrada")


class LoteDuplicado(Exception):
    def __init__(self, codigo: str):
        self.codigo = codigo
        super().__init__(f"El lote {codigo} ya existe")
