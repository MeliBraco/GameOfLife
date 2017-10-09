class PatronInvalido(Exception):

    def __init__(self):
        self.msg = "El patron ingresado esta fuera del rango correspondiente"

    def get_msg(self):
        return self.msg