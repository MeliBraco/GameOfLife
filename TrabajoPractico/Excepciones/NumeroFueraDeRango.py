class NumeroFueraDeRango(Exception):
    def __init__(self):
        self.msg = "El valor ingresado es incorrecto"

    def get_msg(self):
        return self.msg
