class ValorCelularNoValido(Exception):
    ''' SE INGRESA * / -'''

    def __init__(self):
        self.msg = "Debe ingresar * / - "

    def get_msg(self):
        return self.msg